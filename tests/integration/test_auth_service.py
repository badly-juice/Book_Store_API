import pytest

from app.core.security import hash_password
from app.exceptions.all_exceptions import InvalidCredentialsError
from app.models.user import User
from app.services.auth import AuthService


@pytest.mark.asyncio
async def test_login_returns_tokens(session):
    user = User(
        name="Alice",
        email="alice@example.com",
        password_hash=hash_password("secret123"),
    )

    session.add(user)
    await session.commit()

    service = AuthService(session)

    token = await service.login(
        email="alice@example.com",
        password="secret123",
    )

    assert token.access_token
    assert token.refresh_token
    assert token.access_token != token.refresh_token


@pytest.mark.asyncio
async def test_login_with_wrong_password_fails(session):
    user = User(
        name="Alice",
        email="alice@example.com",
        password_hash=hash_password("secret123"),
    )

    session.add(user)
    await session.commit()

    service = AuthService(session)

    with pytest.raises(InvalidCredentialsError):
        await service.login(
            email="alice@example.com",
            password="wrong-password",
        )


@pytest.mark.asyncio
async def test_login_with_unknown_email_fails(session):
    service = AuthService(session)

    with pytest.raises(InvalidCredentialsError):
        await service.login(
            email="unknown@example.com",
            password="secret123",
        )


@pytest.mark.asyncio
async def test_refresh_returns_new_tokens(session):
    user = User(
        name="Alice",
        email="alice@example.com",
        password_hash=hash_password("secret123"),
    )

    session.add(user)
    await session.commit()

    service = AuthService(session)

    first_token = await service.login(
        email="alice@example.com",
        password="secret123",
    )

    refreshed_token = await service.refresh(first_token.refresh_token)

    assert refreshed_token.access_token
    assert refreshed_token.refresh_token
