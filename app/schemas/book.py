import uuid
from decimal import Decimal
from typing import Annotated, Any

from pydantic import BaseModel, ConfigDict, Field, field_validator


class BookBase(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: Annotated[str, Field(min_length=3, max_length=255)]
    author: Annotated[str, Field(min_length=3, max_length=100)]
    description: Annotated[str, Field(min_length=10, max_length=3000)]
    price: Annotated[Decimal, Field(gt=0, max_digits=10, decimal_places=2)]
    stock: Annotated[int, Field(ge=0)] = 0
    isbn: Annotated[str, Field(min_length=10, max_length=20)]


class BookCreate(BookBase):
    category_ids: list[uuid.UUID] = Field(default_factory=list)


class BookRead(BookBase):
    model_config = ConfigDict(from_attributes=True, extra="forbid")

    id: uuid.UUID
    category_ids: list[uuid.UUID] = Field(validation_alias="book_categories")

    @field_validator("category_ids", mode="before")
    @classmethod
    def _extract_category_ids(cls, value: Any) -> list[uuid.UUID]:
        category_ids: list[uuid.UUID] = []

        for item in value or []:
            category_ids.append(getattr(item, "category_id", item))

        return category_ids


class BookUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: Annotated[str | None, Field(min_length=3, max_length=255)] = None
    author: Annotated[str | None, Field(min_length=3, max_length=100)] = None
    description: Annotated[str | None, Field(min_length=10, max_length=3000)] = None
    price: Annotated[Decimal | None, Field(gt=0, max_digits=10, decimal_places=2)] = None
    stock: Annotated[int | None, Field(ge=0)] = None
    isbn: Annotated[str | None, Field(min_length=10, max_length=20)] = None
    category_ids: list[uuid.UUID] | None = None
