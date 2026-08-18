from typing import TYPE_CHECKING

from sqlalchemy import Enum, String, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base

from .enums import UserRole
from .mixins import UUIDTimestampMixin

if TYPE_CHECKING:
    from .order import Order


class User(Base, UUIDTimestampMixin):
    __tablename__ = "users"

    role: Mapped[UserRole] = mapped_column(
        Enum(UserRole, name="user_role"),
        default=UserRole.USER,
        server_default=text("'USER'"),
        nullable=False,
    )

    name: Mapped[str] = mapped_column(String(100), nullable=False)

    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)

    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)

    orders: Mapped[list["Order"]] = relationship(back_populates="user")
