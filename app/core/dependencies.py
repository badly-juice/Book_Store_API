from typing import Annotated
from uuid import UUID

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import decode_access_token, oauth2_scheme
from app.database.session import async_session
from app.exceptions.all_exceptions import (
    InvalidCredentialsError,
    InvalidTokenError,
    PermissionDeniedError,
)
from app.models.enums import UserRole
from app.models.user import User
from app.repositories.user import UserRepository


async def get_session():
    async with async_session() as session:
        yield session


SessionDep = Annotated[AsyncSession, Depends(get_session)]


async def get_current_user(
    session: SessionDep, token: Annotated[str, Depends(oauth2_scheme)]
) -> User:
    payload = decode_access_token(token)
    user_id = payload.get("sub")

    try:
        user_uuid = UUID(user_id)
    except (KeyError, ValueError, TypeError):
        raise InvalidTokenError() from None

    repository = UserRepository(session)
    user = await repository.get(user_uuid)

    if user is None:
        raise InvalidCredentialsError()

    return user


CurrentUserDep = Annotated[User, Depends(get_current_user)]


async def get_current_admin(current_user: CurrentUserDep) -> User:
    if current_user.role != UserRole.ADMIN:
        raise PermissionDeniedError()

    return current_user


CurrentAdminDep = Annotated[User, Depends(get_current_admin)]
