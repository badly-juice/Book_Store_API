from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.order import Order
from app.models.order_item import OrderItem
from app.repositories.base import BaseRepository


class OrderRepository(BaseRepository[Order]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, Order)

    async def get_with_items(self, order_id: UUID) -> Order | None:
        stmt = (
            select(Order)
            .where(Order.id == order_id)
            .options(selectinload(Order.order_items).selectinload(OrderItem.book))
        )
        return await self.session.scalar(stmt)

    async def get_with_items_for_update(self, order_id: UUID) -> Order | None:
        stmt = (
            select(Order)
            .where(Order.id == order_id)
            .options(selectinload(Order.order_items).selectinload(OrderItem.book))
            .with_for_update()
        )
        return await self.session.scalar(stmt)

    async def list_with_items(self, user_id: UUID | None = None) -> list[Order]:
        stmt = (
            select(Order)
            .options(selectinload(Order.order_items).selectinload(OrderItem.book))
            .order_by(Order.created_at.desc())
        )

        if user_id is not None:
            stmt = stmt.where(Order.user_id == user_id)

        result = await self.session.scalars(stmt)
        return list(result.all())
