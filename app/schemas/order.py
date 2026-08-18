import uuid
from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict

from app.models.enums import OrderStatus
from app.schemas.order_item import OrderItemCreate, OrderItemRead


class OrderBase(BaseModel):
    model_config = ConfigDict(extra="forbid")


class OrderCreate(OrderBase):
    items: list[OrderItemCreate]


class OrderRead(OrderBase):
    model_config = ConfigDict(from_attributes=True, extra="forbid")

    id: uuid.UUID
    user_id: uuid.UUID
    status: OrderStatus
    total_price: Decimal
    created_at: datetime
    updated_at: datetime
    order_items: list[OrderItemRead]
