from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base

from .mixins import UUIDTimestampMixin

if TYPE_CHECKING:
    from .book_category import BookCategory


class Category(Base, UUIDTimestampMixin):
    __tablename__ = "categories"

    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True, index=True)

    book_categories: Mapped[list["BookCategory"]] = relationship(
        back_populates="category",
        cascade="all, delete-orphan",
    )
