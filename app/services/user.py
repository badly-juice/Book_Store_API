import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import hash_password
from app.exceptions.all_exceptions import (
    PermissionDeniedError,
    UserAlreadyExistsError,
    UserNotFoundError,
)
from app.models.enums import UserRole
from app.models.user import User
from app.repositories.user import UserRepository
from app.schemas.user import UserCreate, UserUpdate
from app.services.base import BaseService


class UserService(BaseService):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session)
        self.user_repository = UserRepository(session)

    async def get_by_id(self, user_id: uuid.UUID) -> User:
        user = await self.user_repository.get_by_id(user_id)

        if user is None:
            raise UserNotFoundError()

        return user

    async def get_users(self) -> list[User]:
        return await self.user_repository.list_all_users()

    async def register(self, user_data: UserCreate) -> User:
        existing_user = await self.user_repository.get_by_email(user_data.email)

        if existing_user is not None:
            raise UserAlreadyExistsError()

        data = user_data.model_dump(exclude={"password"})
        user = await self.user_repository.create(
            **data,
            password_hash=hash_password(user_data.password),
        )

        await self.commit()

        return user

    async def update_profile(
        self,
        user_id: uuid.UUID,
        user_data: UserUpdate,
        current_user: User,
    ) -> User:
        if current_user.id != user_id and current_user.role != UserRole.ADMIN:
            raise PermissionDeniedError()

        user = await self.get_by_id(user_id)

        await self.user_repository.update(
            user,
            **user_data.model_dump(exclude_unset=True),
        )
        await self.commit()
        return user
