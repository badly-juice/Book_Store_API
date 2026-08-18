from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.exceptions.all_exceptions import (
    BookAlreadyExistsError,
    BookNotFoundError,
    CategoryNotFoundError,
)
from app.models.book import Book
from app.models.book_category import BookCategory
from app.repositories.book import BookRepository
from app.repositories.category import CategoryRepository
from app.schemas.book import BookCreate, BookUpdate
from app.services.base import BaseService


class BookService(BaseService):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session)
        self.book_repository = BookRepository(session)
        self.category_repository = CategoryRepository(session)

    async def get_book(self, book_id: UUID) -> Book:
        book = await self.book_repository.get_with_categories(book_id)

        if book is None:
            raise BookNotFoundError()

        return book

    async def get_books(self) -> list[Book]:
        return await self.book_repository.list_with_categories()

    async def _check_isbn_exists(self, isbn: str, exclude_id: UUID | None = None) -> None:
        book = await self.book_repository.get_by_isbn(isbn)

        if book is not None and book.id != exclude_id:
            raise BookAlreadyExistsError()

    async def _apply_categories(self, book: Book, category_ids: list[UUID]) -> None:
        requested_category_ids = set(category_ids)
        categories = await self.category_repository.get_by_ids(
            requested_category_ids
        )

        if len(categories) != len(requested_category_ids):
            raise CategoryNotFoundError()

        book.book_categories.clear()
        await self.session.flush()

        for category in categories:
            book.book_categories.append(BookCategory(category_id=category.id))

    async def create_book(self, book_data: BookCreate) -> Book:
        await self._check_isbn_exists(book_data.isbn)

        requested_category_ids = set(book_data.category_ids)
        categories = await self.category_repository.get_by_ids(
            requested_category_ids
        )

        if len(categories) != len(requested_category_ids):
            raise CategoryNotFoundError()

        book = await self.book_repository.create(
            **book_data.model_dump(exclude={"category_ids"}),
        )

        await self.session.refresh(book, attribute_names=["book_categories"])

        for category in categories:
            book.book_categories.append(
                BookCategory(category_id=category.id)
            )

        await self.commit()

        return await self.get_book(book.id)

    async def update_book(self, book_id: UUID, book_data: BookUpdate) -> Book:
        book = await self.get_book(book_id)

        update_data = book_data.model_dump(
            exclude_unset=True,
            exclude={"category_ids"},
        )

        if "isbn" in update_data:
            await self._check_isbn_exists(
                update_data["isbn"],
                exclude_id=book.id,
            )

        await self.book_repository.update(book, **update_data)

        if book_data.category_ids is not None:
            await self._apply_categories(book, book_data.category_ids)

        await self.commit()

        return await self.get_book(book.id)

    async def delete_book(self, book_id: UUID) -> None:
        book = await self.get_book(book_id)

        await self.book_repository.delete(book)
        await self.commit()
