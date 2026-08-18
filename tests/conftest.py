from collections.abc import Callable
from dataclasses import dataclass
from datetime import UTC, datetime
from decimal import Decimal
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

import app.main as main_module
from app.api.deps import (
    get_auth_service,
    get_book_service,
    get_category_service,
    get_order_service,
    get_user_service,
)
from app.core.dependencies import get_current_admin, get_current_user
from app.models.enums import OrderStatus, UserRole
from app.schemas.user import Token


@dataclass
class UserDTO:
    id: UUID
    name: str
    email: str
    role: UserRole


@dataclass
class CategoryDTO:
    id: UUID
    name: str


@dataclass
class CategoryLinkDTO:
    category_id: UUID


@dataclass
class BookDTO:
    id: UUID
    title: str
    author: str
    description: str
    price: Decimal
    stock: int
    isbn: str
    book_categories: list[CategoryLinkDTO]


@dataclass
class OrderItemDTO:
    id: UUID
    order_id: UUID
    book_id: UUID
    quantity: int
    price: Decimal


@dataclass
class OrderDTO:
    id: UUID
    user_id: UUID
    status: OrderStatus
    total_price: Decimal
    created_at: datetime
    updated_at: datetime
    order_items: list[OrderItemDTO]


class FakeAuthService:
    async def login(self, email: str, password: str) -> Token:
        return Token(access_token="fake-access-token", refresh_token="fake-refresh-token")


class FakeUserService:
    async def register(self, user_data) -> UserDTO:
        return UserDTO(
            id=uuid4(),
            name=user_data.name,
            email=user_data.email,
            role=UserRole.USER,
        )

    async def get_users(self) -> list[UserDTO]:
        return [
            UserDTO(
                id=uuid4(),
                name="Alice",
                email="alice@example.com",
                role=UserRole.USER,
            )
        ]

    async def get_by_id(self, user_id: UUID) -> UserDTO:
        return UserDTO(
            id=user_id,
            name="Alice",
            email="alice@example.com",
            role=UserRole.USER,
        )

    async def update_profile(
        self,
        user_id: UUID,
        user_data,
        current_user: UserDTO,
    ) -> UserDTO:
        return UserDTO(
            id=user_id,
            name=user_data.name or current_user.name,
            email=user_data.email or current_user.email,
            role=current_user.role,
        )


class FakeBookService:
    async def get_books(self) -> list[BookDTO]:
        return [
            BookDTO(
                id=uuid4(),
                title="The Pragmatic Book",
                author="Jane Doe",
                description="A useful developer book.",
                price=Decimal("19.99"),
                stock=10,
                isbn="1234567890",
                book_categories=[CategoryLinkDTO(uuid4())],
            )
        ]

    async def get_book(self, book_id: UUID) -> BookDTO:
        return BookDTO(
            id=book_id,
            title="The Pragmatic Book",
            author="Jane Doe",
            description="A useful developer book.",
            price=Decimal("19.99"),
            stock=10,
            isbn="1234567890",
            book_categories=[],
        )


class FakeCategoryService:
    async def get_categories(self) -> list[CategoryDTO]:
        return [
            CategoryDTO(
                id=uuid4(),
                name="Programming",
            )
        ]

    async def get_category(self, category_id: UUID) -> CategoryDTO:
        return CategoryDTO(
            id=category_id,
            name="Programming",
        )


class FakeOrderService:
    async def create_order(self, current_user: UserDTO) -> OrderDTO:
        order_id = uuid4()

        return OrderDTO(
            id=order_id,
            user_id=current_user.id,
            status=OrderStatus.PENDING,
            total_price=Decimal("0"),
            created_at=datetime.now(UTC),
            updated_at=datetime.now(UTC),
            order_items=[],
        )


@pytest.fixture
def build_client():
    async def noop_create_admin() -> None:
        return None

    main_module.create_admin = noop_create_admin

    def _build_client(overrides: dict[Callable, Callable]) -> TestClient:
        main_module.app.dependency_overrides.clear()
        main_module.app.dependency_overrides.update(overrides)
        return TestClient(main_module.app)

    yield _build_client

    main_module.app.dependency_overrides.clear()


@pytest.fixture
def user() -> UserDTO:
    return UserDTO(
        id=uuid4(),
        name="Alice",
        email="alice@example.com",
        role=UserRole.USER,
    )


@pytest.fixture
def admin() -> UserDTO:
    return UserDTO(
        id=uuid4(),
        name="Admin",
        email="admin@example.com",
        role=UserRole.ADMIN,
    )
