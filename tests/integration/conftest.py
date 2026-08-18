import pytest_asyncio
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import NullPool

from app.core.config import settings
from app.models.book import Book
from app.models.book_category import BookCategory
from app.models.category import Category
from app.models.order import Order
from app.models.order_item import OrderItem
from app.models.user import User

test_engine = create_async_engine(
    settings.database_url,
    echo=True,
    poolclass=NullPool,
)

test_session = async_sessionmaker(
    bind=test_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


@pytest_asyncio.fixture
async def session() -> AsyncSession:
    async with test_session() as session:
        yield session

    async with test_session() as cleanup_session:
        await cleanup_session.execute(delete(OrderItem))
        await cleanup_session.execute(delete(Order))
        await cleanup_session.execute(delete(BookCategory))
        await cleanup_session.execute(delete(Book))
        await cleanup_session.execute(delete(Category))
        await cleanup_session.execute(delete(User))
        await cleanup_session.commit()
