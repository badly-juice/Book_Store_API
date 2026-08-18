from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, Integer, Numeric, String, Text, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base

from .mixins import UUIDTimestampMixin

if TYPE_CHECKING:
    from .book_category import BookCategory
    from .order_item import OrderItem


class Book(Base, UUIDTimestampMixin):
    __tablename__ = "books"

    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    author: Mapped[str] = mapped_column(String(100), nullable=False)

    description: Mapped[str] = mapped_column(Text, nullable=False)

    price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)

    stock: Mapped[int] = mapped_column(
        Integer, default=0, server_default=text("0"), nullable=False
    )

    isbn: Mapped[str] = mapped_column(String(20), nullable=False, unique=True)

    order_items: Mapped[list["OrderItem"]] = relationship(back_populates="book")

    book_categories: Mapped[list["BookCategory"]] = relationship(
        back_populates="book", cascade="all, delete-orphan"
    )

    __table_args__ = (
        CheckConstraint(
            "price >= 0",
            name="ck_books_price_positive",
        ),
        CheckConstraint(
            "stock >= 0",
            name="ck_books_stock_positive",
        ),
    )
