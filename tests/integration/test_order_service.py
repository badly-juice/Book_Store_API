from decimal import Decimal

import pytest

from app.core.security import hash_password
from app.exceptions.all_exceptions import (
    InsufficientStockError,
    OrderAlreadyCancelledError,
)
from app.models.book import Book
from app.models.enums import OrderStatus, UserRole
from app.models.user import User
from app.schemas.order_item import OrderItemCreate
from app.services.order import OrderService


async def create_user(session) -> User:
    user = User(
        name="Alice",
        email="alice@example.com",
        password_hash=hash_password("secret123"),
        role=UserRole.USER,
    )

    session.add(user)
    await session.commit()

    return user


async def create_book(session, stock: int = 10) -> Book:
    book = Book(
        title="Python Book",
        author="John Doe",
        description="Python programming",
        price=Decimal("20.00"),
        stock=stock,
        isbn="9999999999",
    )

    session.add(book)
    await session.commit()

    return book


@pytest.mark.asyncio
async def test_create_order(session):
    user = await create_user(session)

    service = OrderService(session)

    order = await service.create_order(user)

    assert order.id is not None
    assert order.user_id == user.id
    assert order.status == OrderStatus.PENDING
    assert order.total_price == Decimal("0")
    assert order.order_items == []


@pytest.mark.asyncio
async def test_add_item_to_order(session):
    user = await create_user(session)
    book = await create_book(session, stock=10)

    service = OrderService(session)

    order = await service.create_order(user)

    updated_order = await service.add_item(
        order.id,
        OrderItemCreate(
            book_id=book.id,
            quantity=2,
        ),
        user,
    )

    assert len(updated_order.order_items) == 1

    item = updated_order.order_items[0]

    assert item.book_id == book.id
    assert item.quantity == 2
    assert item.price == Decimal("20.00")
    assert updated_order.total_price == Decimal("40.00")

    await session.refresh(book)

    assert book.stock == 8


@pytest.mark.asyncio
async def test_add_same_book_increases_quantity(session):
    user = await create_user(session)
    book = await create_book(session, stock=10)

    service = OrderService(session)

    order = await service.create_order(user)

    await service.add_item(
        order.id,
        OrderItemCreate(
            book_id=book.id,
            quantity=2,
        ),
        user,
    )

    updated_order = await service.add_item(
        order.id,
        OrderItemCreate(
            book_id=book.id,
            quantity=3,
        ),
        user,
    )

    assert len(updated_order.order_items) == 1
    assert updated_order.order_items[0].quantity == 5
    assert updated_order.total_price == Decimal("100.00")

    await session.refresh(book)

    assert book.stock == 5


@pytest.mark.asyncio
async def test_add_item_with_insufficient_stock_fails(session):
    user = await create_user(session)
    book = await create_book(session, stock=2)

    service = OrderService(session)

    order = await service.create_order(user)

    with pytest.raises(InsufficientStockError):
        await service.add_item(
            order.id,
            OrderItemCreate(
                book_id=book.id,
                quantity=3,
            ),
            user,
        )

    await session.refresh(book)

    assert book.stock == 2


@pytest.mark.asyncio
async def test_cancel_order_restores_stock(session):
    user = await create_user(session)
    book = await create_book(session, stock=10)

    service = OrderService(session)

    order = await service.create_order(user)

    await service.add_item(
        order.id,
        OrderItemCreate(
            book_id=book.id,
            quantity=4,
        ),
        user,
    )

    await session.refresh(book)
    assert book.stock == 6

    cancelled_order = await service.cancel_order(
        order.id,
        user,
    )

    assert cancelled_order.status == OrderStatus.CANCELED

    await session.refresh(book)

    assert book.stock == 10


@pytest.mark.asyncio
async def test_cancel_order_twice_fails(session):
    user = await create_user(session)
    book = await create_book(session)

    service = OrderService(session)

    order = await service.create_order(user)

    await service.cancel_order(order.id, user)

    with pytest.raises(OrderAlreadyCancelledError):
        await service.cancel_order(order.id, user)
