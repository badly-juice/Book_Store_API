from collections.abc import Sequence
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.category import Category
from app.repositories.base import BaseRepository


class CategoryRepository(BaseRepository[Category]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, Category)

    async def get_by_ids(self, category_ids: Sequence[UUID]) -> list[Category]:
        if not category_ids:
            return []

        stmt = select(Category).where(Category.id.in_(category_ids))
        result = await self.session.scalars(stmt)
        return list(result.all())

    async def list_all_categories(self) -> list[Category]:
        stmt = select(Category).order_by(Category.created_at.desc())
        result = await self.session.scalars(stmt)
        return list(result.all())
        