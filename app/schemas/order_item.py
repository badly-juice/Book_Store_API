import uuid
from decimal import Decimal
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field


class OrderItemBase(BaseModel):
    model_config = ConfigDict(extra="forbid")

    quantity: Annotated[int, Field(gt=0)]


class OrderItemCreate(OrderItemBase):
    book_id: uuid.UUID


class OrderItemRead(OrderItemBase):
    model_config = ConfigDict(from_attributes=True, extra="forbid")

    id: uuid.UUID
    order_id: uuid.UUID
    book_id: uuid.UUID
    price: Annotated[Decimal, Field(gt=0, max_digits=10, decimal_places=2)]


class OrderItemUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    quantity: Annotated[int | None, Field(gt=0)] = None
