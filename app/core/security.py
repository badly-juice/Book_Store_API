from datetime import UTC, datetime, timedelta

import bcrypt
from fastapi.security import OAuth2PasswordBearer
from jwt import ExpiredSignatureError
from jwt import InvalidTokenError as JWTInvalidTokenError
from jwt import decode as jwt_decode
from jwt import encode as jwt_encode

from app.core.config import settings
from app.exceptions.all_exceptions import (
    ExpiredTokenError,
    InvalidTokenError,
)


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(password: str, hashed_password: str) -> bool:
    try:
        return bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))
    except ValueError:
        return False


def create_access_token(user_id: str, role: str) -> str:
    expire = datetime.now(UTC) + timedelta(minutes=settings.access_token_expire_minutes)

    payload = {
        "sub": user_id,
        "role": role,
        "type": "access",
        "exp": expire,
    }

    return jwt_encode(
        payload,
        settings.secret_key.get_secret_value(),
        algorithm=settings.algorithm,
    )


def create_refresh_token(user_id: str) -> str:
    expire = datetime.now(UTC) + timedelta(days=settings.refresh_token_expire_days)

    payload = {
        "sub": user_id,
        "type": "refresh",
        "exp": expire,
    }

    return jwt_encode(
        payload,
        settings.secret_key.get_secret_value(),
        algorithm=settings.algorithm,
    )


def decode_access_token(token: str) -> dict:
    try:
        payload = jwt_decode(
            token,
            settings.secret_key.get_secret_value(),
            algorithms=[settings.algorithm],
        )

        if payload.get("type") != "access":
            raise InvalidTokenError()

        return payload

    except ExpiredSignatureError:
        raise ExpiredTokenError() from None
    except JWTInvalidTokenError:
        raise InvalidTokenError() from None


def decode_refresh_token(token: str) -> dict:
    try:
        payload = jwt_decode(
            token,
            settings.secret_key.get_secret_value(),
            algorithms=[settings.algorithm],
        )

        if payload.get("type") != "refresh":
            raise InvalidTokenError()

        return payload

    except ExpiredSignatureError:
        raise ExpiredTokenError() from None
    except JWTInvalidTokenError:
        raise InvalidTokenError() from None


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")
