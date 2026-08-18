import uuid
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import Enum, ForeignKey, Numeric, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base

from .enums import OrderStatus
from .mixins import UUIDTimestampMixin

if TYPE_CHECKING:
    from .order_item import OrderItem
    from .user import User


class Order(Base, UUIDTimestampMixin):
    __tablename__ = "orders"

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True
    )

    status: Mapped[OrderStatus] = mapped_column(
        Enum(OrderStatus, name="order_status"),
        default=OrderStatus.PENDING,
        server_default=text("'PENDING'"),
        nullable=False,
    )

    total_price: Mapped[Decimal] = mapped_column(
        Numeric(10, 2), default=0, server_default=text("0"), nullable=False
    )

    user: Mapped["User"] = relationship(back_populates="orders")

    order_items: Mapped[list["OrderItem"]] = relationship(back_populates="order")
