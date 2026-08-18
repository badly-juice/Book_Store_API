from decimal import Decimal
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.exceptions.all_exceptions import (
    BookNotFoundError,
    InsufficientStockError,
    OrderAlreadyCancelledError,
    OrderCannotBeCancelledError,
    OrderModificationError,
    OrderNotFoundError,
    PermissionDeniedError,
)
from app.models.enums import OrderStatus, UserRole
from app.models.order import Order
from app.models.user import User
from app.repositories.book import BookRepository
from app.repositories.order import OrderRepository
from app.repositories.order_item import OrderItemRepository
from app.schemas.order_item import OrderItemCreate
from app.services.base import BaseService


class OrderService(BaseService):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session)
        self.book_repository = BookRepository(session)
        self.order_item_repository = OrderItemRepository(session)
        self.order_repository = OrderRepository(session)

    async def get_order(self, order_id: UUID, current_user: User) -> Order:
        order = await self.order_repository.get_with_items(order_id)

        if order is None:
            raise OrderNotFoundError()

        if current_user.role != UserRole.ADMIN and order.user_id != current_user.id:
            raise PermissionDeniedError()

        return order

    async def get_orders(self, current_user: User) -> list[Order]:
        if current_user.role == UserRole.ADMIN:
            return await self.order_repository.list_with_items()

        return await self.order_repository.list_with_items(user_id=current_user.id)

    async def create_order(self, current_user: User) -> Order:
        order = await self.order_repository.create(
            user_id=current_user.id,
            status=OrderStatus.PENDING,
            total_price=Decimal("0"),
        )

        await self.commit()

        return await self.get_order(order.id, current_user)

    async def cancel_order(self, order_id: UUID, current_user: User) -> Order:
        order = await self.order_repository.get_with_items_for_update(order_id)

        if order is None:
            raise OrderNotFoundError()

        if current_user.role != UserRole.ADMIN and order.user_id != current_user.id:
            raise PermissionDeniedError()

        if order.status == OrderStatus.CANCELED:
            raise OrderAlreadyCancelledError()

        if order.status in {OrderStatus.PAID, OrderStatus.SHIPPED, OrderStatus.DELIVERED}:
            raise OrderCannotBeCancelledError()

        for item in order.order_items:
            book = await self.book_repository.get_for_update(item.book_id)

            if book is not None:
                book.stock += item.quantity

        order.status = OrderStatus.CANCELED

        await self.commit()

        return await self.get_order(order.id, current_user)

    async def _recalculate_total(self, order: Order) -> None:
        total = Decimal("0")

        for item in order.order_items:
            total += item.price * item.quantity

        order.total_price = total

    async def add_item(
        self, order_id: UUID, item_data: OrderItemCreate, current_user: User
    ) -> Order:
        order = await self.order_repository.get_with_items_for_update(order_id)

        if order is None:
            raise OrderNotFoundError()

        if current_user.role != UserRole.ADMIN and order.user_id != current_user.id:
            raise PermissionDeniedError()

        if order.status != OrderStatus.PENDING:
            raise OrderModificationError()

        book = await self.book_repository.get_for_update(item_data.book_id)

        if book is None:
            raise BookNotFoundError()

        if book.stock < item_data.quantity:
            raise InsufficientStockError()

        order_item = await self.order_item_repository.get_by_order_and_book_for_update(
            order.id, book.id
        )

        if order_item is None:
            await self.order_item_repository.create(
                order_id=order.id,
                book_id=book.id,
                quantity=item_data.quantity,
                price=book.price,
            )
        else:
            order_item.quantity += item_data.quantity

        book.stock -= item_data.quantity

        await self.session.refresh(order, attribute_names=["order_items"])
        await self._recalculate_total(order)

        await self.commit()

        return await self.get_order(order.id, current_user)
