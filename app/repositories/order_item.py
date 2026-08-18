from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.order_item import OrderItem
from app.repositories.base import BaseRepository


class OrderItemRepository(BaseRepository[OrderItem]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, OrderItem)

    async def get_by_order_and_book(self, order_id: UUID, book_id: UUID) -> OrderItem | None:
        stmt = select(OrderItem).where(
            OrderItem.order_id == order_id, OrderItem.book_id == book_id
        )
        return await self.session.scalar(stmt)

    async def get_by_order_and_book_for_update(
        self, order_id: UUID, book_id: UUID
    ) -> OrderItem | None:
        stmt = (
            select(OrderItem)
            .where(OrderItem.order_id == order_id, OrderItem.book_id == book_id)
            .with_for_update()
        )
        return await self.session.scalar(stmt)
