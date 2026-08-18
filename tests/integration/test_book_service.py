from decimal import Decimal
from uuid import uuid4

import pytest

from app.exceptions.all_exceptions import BookNotFoundError, CategoryNotFoundError
from app.schemas.book import BookCreate, BookUpdate
from app.schemas.category import CategoryCreate
from app.services.book import BookService
from app.services.category import CategoryService


@pytest.mark.asyncio
async def test_create_book_with_categories(session):
    category_service = CategoryService(session)
    book_service = BookService(session)

    category = await category_service.create_category(CategoryCreate(name="Programming"))

    created_book = await book_service.create_book(
        BookCreate(
            title="Python Book",
            author="John Doe",
            description="Python programming",
            price=Decimal("29.99"),
            stock=10,
            isbn="1234567890",
            category_ids=[category.id],
        )
    )

    book = await book_service.get_book(created_book.id)

    assert book.id is not None
    assert book.title == "Python Book"
    assert book.stock == 10
    assert book.price == Decimal("29.99")
    assert len(book.book_categories) == 1
    assert book.book_categories[0].category_id == category.id


@pytest.mark.asyncio
async def test_get_book_with_categories(session):
    category_service = CategoryService(session)
    book_service = BookService(session)

    category = await category_service.create_category(CategoryCreate(name="Programming"))

    created_book = await book_service.create_book(
        BookCreate(
            title="Python Book",
            author="John Doe",
            description="Python programming",
            price=Decimal("29.99"),
            stock=10,
            isbn="1234567891",
            category_ids=[category.id],
        )
    )

    result = await book_service.get_book(created_book.id)

    assert result.id == created_book.id
    assert result.title == "Python Book"
    assert len(result.book_categories) == 1
    assert result.book_categories[0].category_id == category.id


@pytest.mark.asyncio
async def test_update_book(session):
    category_service = CategoryService(session)
    book_service = BookService(session)

    category = await category_service.create_category(CategoryCreate(name="Programming"))

    created_book = await book_service.create_book(
        BookCreate(
            title="Python Book",
            author="John Doe",
            description="Python programming",
            price=Decimal("29.99"),
            stock=10,
            isbn="1234567892",
            category_ids=[category.id],
        )
    )

    await book_service.update_book(
        created_book.id,
        BookUpdate(title="Advanced Python"),
    )

    updated = await book_service.get_book(created_book.id)

    assert updated.id == created_book.id
    assert updated.title == "Advanced Python"
    assert updated.price == Decimal("29.99")
    assert updated.stock == 10


@pytest.mark.asyncio
async def test_delete_book(session):
    book_service = BookService(session)

    book = await book_service.create_book(
        BookCreate(
            title="Python Book",
            author="John Doe",
            description="Python programming",
            price=Decimal("29.99"),
            stock=10,
            isbn="1234567893",
            category_ids=[],
        )
    )

    await book_service.delete_book(book.id)

    with pytest.raises(BookNotFoundError):
        await book_service.get_book(book.id)


@pytest.mark.asyncio
async def test_create_book_with_missing_category_fails(session):
    book_service = BookService(session)

    with pytest.raises(CategoryNotFoundError):
        await book_service.create_book(
            BookCreate(
                title="Python Book",
                author="John Doe",
                description="Python programming",
                price=Decimal("29.99"),
                stock=10,
                isbn="1234567894",
                category_ids=[uuid4()],
            )
        )
