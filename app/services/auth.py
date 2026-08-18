from app.core.security import (
    create_access_token,
    create_refresh_token,
    decode_refresh_token,
    verify_password,
)
from app.exceptions.all_exceptions import InvalidCredentialsError
from app.repositories.user import UserRepository
from app.schemas.user import Token
from app.services.base import BaseService


class AuthService(BaseService):
    def __init__(self, session) -> None:
        super().__init__(session)
        self.user_repository = UserRepository(session)

    async def login(self, email: str, password: str) -> Token:
        user = await self.user_repository.get_by_email(email)

        if user is None:
            raise InvalidCredentialsError()

        if not verify_password(password, user.password_hash):
            raise InvalidCredentialsError()

        access_token = create_access_token(
            user_id=str(user.id),
            role=user.role.name,
        )

        refresh_token = create_refresh_token(user_id=str(user.id))

        return Token(
            access_token=access_token,
            refresh_token=refresh_token,
        )

    async def refresh(self, refresh_token: str) -> Token:
        payload = decode_refresh_token(refresh_token)

        user_id = payload.get("sub")

        if not user_id:
            raise InvalidCredentialsError()

        user = await self.user_repository.get_by_id(user_id)

        if user is None:
            raise InvalidCredentialsError()

        access_token = create_access_token(
            user_id=str(user.id),
            role=user.role.name,
        )

        new_refresh_token = create_refresh_token(user_id=str(user.id))

        return Token(
            access_token=access_token,
            refresh_token=new_refresh_token,
        )
