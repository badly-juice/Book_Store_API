import uuid
from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.base import Base


class BaseRepository[Model: Base]:
    def __init__(self, session: AsyncSession, model: type[Model]) -> None:
        self.session = session
        self.model = model

    async def get(self, id: uuid.UUID) -> Model | None:
        return await self.session.get(self.model, id)

    async def get_by_id(self, id: uuid.UUID) -> Model | None:
        return await self.get(id)

    async def get_all(self) -> list[Model]:
        stmt = select(self.model)
        result = await self.session.scalars(stmt)
        return list(result.all())

    async def create(self, **kwargs: Any) -> Model:
        obj = self.model(**kwargs)
        self.session.add(obj)
        await self.session.flush()
        await self.session.refresh(obj)
        return obj

    async def update(self, obj: Model, **kwargs: Any) -> Model:
        for field, value in kwargs.items():
            setattr(obj, field, value)
        await self.session.flush()
        await self.session.refresh(obj)
        return obj

    async def delete(self, obj: Model) -> None:
        await self.session.delete(obj)
        await self.session.flush()
