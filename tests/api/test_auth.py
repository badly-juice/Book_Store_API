from app.api.deps import get_auth_service, get_user_service


def test_login_returns_token(build_client) -> None:
    from tests.conftest import FakeAuthService

    client = build_client(
        {
            get_auth_service: lambda: FakeAuthService(),
        }
    )

    with client:
        response = client.post(
            "/api/v1/auth/login",
            data={
                "username": "alice@example.com",
                "password": "secret123",
            },
        )

    assert response.status_code == 200

    data = response.json()

    assert data["access_token"] == "fake-access-token"
    assert data["refresh_token"] == "fake-refresh-token"
    assert data["token_type"] == "bearer"


def test_register_returns_user(build_client) -> None:
    from tests.conftest import FakeUserService

    client = build_client(
        {
            get_user_service: lambda: FakeUserService(),
        }
    )

    payload = {
        "name": "Alice",
        "email": "alice@example.com",
        "password": "secret123",
    }

    with client:
        response = client.post(
            "/api/v1/auth/register",
            json=payload,
        )

    assert response.status_code == 201

    data = response.json()

    assert data["name"] == "Alice"
    assert data["email"] == "alice@example.com"
    assert data["role"] == "user"
    assert "password" not in data
    assert "password_hash" not in data
