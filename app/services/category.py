from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.exceptions.all_exceptions import CategoryNotFoundError
from app.models.category import Category
from app.repositories.category import CategoryRepository
from app.schemas.category import CategoryCreate, CategoryUpdate
from app.services.base import BaseService


class CategoryService(BaseService):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session)
        self.category_repository = CategoryRepository(session)

    async def get_category(self, category_id: UUID) -> Category:
        category = await self.category_repository.get(category_id)

        if category is None:
            raise CategoryNotFoundError()

        return category

    async def get_categories(self) -> list[Category]:
        return await self.category_repository.list_all_categories()

    async def create_category(self, category_data: CategoryCreate) -> Category:
        category = await self.category_repository.create(**category_data.model_dump())

        await self.commit()

        return category

    async def update_category(
        self, category_id: UUID, category_data: CategoryUpdate
    ) -> Category:
        category = await self.get_category(category_id)

        update_data = category_data.model_dump(exclude_unset=True)

        if update_data:
            await self.category_repository.update(category, **update_data)

        await self.commit()

        return category

    async def delete_category(self, category_id: UUID) -> None:
        category = await self.get_category(category_id)

        await self.category_repository.delete(category)

        await self.commit()
