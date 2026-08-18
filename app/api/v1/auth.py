from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm

from app.api.deps import AuthServiceDep, UserServiceDep
from app.models.user import User
from app.schemas.user import Token, UserCreate, UserRead

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate, service: UserServiceDep) -> User:
    return await service.register(user_data)


@router.post("/login", response_model=Token)
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], service: AuthServiceDep
) -> Token:
    return await service.login(email=form_data.username, password=form_data.password)


@router.post("/refresh", response_model=Token)
async def refresh(refresh_token: str, service: AuthServiceDep) -> Token:
    return await service.refresh(refresh_token)
