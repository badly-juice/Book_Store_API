import uuid
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base

from .mixins import UUIDTimestampMixin

if TYPE_CHECKING:
    from .book import Book
    from .category import Category


class BookCategory(Base, UUIDTimestampMixin):
    __tablename__ = "book_categories"

    book_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("books.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    category_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("categories.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    book: Mapped["Book"] = relationship(back_populates="book_categories")

    category: Mapped["Category"] = relationship(back_populates="book_categories")

    __table_args__ = (
        UniqueConstraint(
            "book_id",
            "category_id",
            name="uq_book_category",
        ),
    )
