import uuid
from typing import Annotated

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.models.enums import UserRole


class UserBase(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: Annotated[str, Field(min_length=3, max_length=100)]
    email: EmailStr


class UserCreate(UserBase):
    password: Annotated[str, Field(min_length=8, max_length=128)]


class UserRead(UserBase):
    model_config = ConfigDict(from_attributes=True, extra="forbid")

    id: uuid.UUID
    role: UserRole


class UserUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: Annotated[str | None, Field(min_length=3, max_length=100)] = None
    email: EmailStr | None = None


class UserLogin(BaseModel):
    model_config = ConfigDict(extra="forbid")

    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
