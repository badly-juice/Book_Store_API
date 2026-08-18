from uuid import UUID

from fastapi import APIRouter

from app.api.deps import UserServiceDep
from app.core.dependencies import CurrentAdminDep, CurrentUserDep
from app.models.user import User
from app.schemas.user import UserRead, UserUpdate

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", response_model=list[UserRead])
async def get_users(service: UserServiceDep, _: CurrentAdminDep) -> list[User]:
    return await service.get_users()


@router.get("/me", response_model=UserRead)
async def get_me(current_user: CurrentUserDep) -> User:
    return current_user


@router.patch("/me", response_model=UserRead)
async def update_me(
    user_data: UserUpdate,
    service: UserServiceDep,
    current_user: CurrentUserDep,
) -> User:
    return await service.update_profile(current_user.id, user_data, current_user)


@router.get("/{user_id}", response_model=UserRead)
async def get_user(user_id: UUID, service: UserServiceDep, _: CurrentAdminDep) -> User:
    return await service.get_by_id(user_id)


@router.patch("/{user_id}", response_model=UserRead)
async def update_user(
    user_id: UUID,
    user_data: UserUpdate,
    service: UserServiceDep,
    current_admin: CurrentAdminDep,
) -> User:
    return await service.update_profile(user_id, user_data, current_admin)
