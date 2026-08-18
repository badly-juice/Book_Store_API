from collections.abc import Sequence
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.book import Book
from app.models.book_category import BookCategory
from app.repositories.base import BaseRepository


class BookRepository(BaseRepository[Book]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, Book)

    async def get_by_ids_for_update(self, book_ids: Sequence[UUID]) -> list[Book]:
        if not book_ids:
            return []

        stmt = select(Book).where(Book.id.in_(book_ids)).with_for_update()
        result = await self.session.scalars(stmt)
        return list(result.all())

    async def get_for_update(self, book_id: UUID) -> Book | None:
        stmt = select(Book).where(Book.id == book_id).with_for_update()
        return await self.session.scalar(stmt)

    async def get_with_categories(self, book_id: UUID) -> Book | None:
        stmt = (
            select(Book)
            .where(Book.id == book_id)
            .options(selectinload(Book.book_categories).selectinload(BookCategory.category))
        )
        return await self.session.scalar(stmt)

    async def get_by_isbn(self, isbn: str) -> Book | None:
        stmt = select(Book).where(Book.isbn == isbn)
        return await self.session.scalar(stmt)
    
    async def list_with_categories(self) -> list[Book]:
        stmt = (
            select(Book)
            .options(selectinload(Book.book_categories).selectinload(BookCategory.category))
            .order_by(Book.created_at.desc())
        )
        result = await self.session.scalars(stmt)
        return list(result.all())
