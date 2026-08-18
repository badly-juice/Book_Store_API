from app.api.deps import get_user_service
from app.core.dependencies import get_current_admin, get_current_user


def test_get_users_as_admin(build_client, admin) -> None:
    from tests.conftest import FakeUserService

    client = build_client(
        {
            get_current_admin: lambda: admin,
            get_user_service: lambda: FakeUserService(),
        }
    )

    with client:
        response = client.get("/api/v1/users/")

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["role"] == "user"


def test_get_me(build_client, user) -> None:
    client = build_client(
        {
            get_current_user: lambda: user,
        }
    )

    with client:
        response = client.get("/api/v1/users/me")

    assert response.status_code == 200

    assert response.json()["email"] == user.email


def test_update_me(build_client, user) -> None:
    from tests.conftest import FakeUserService

    client = build_client(
        {
            get_current_user: lambda: user,
            get_user_service: lambda: FakeUserService(),
        }
    )

    with client:
        response = client.patch(
            "/api/v1/users/me",
            json={
                "name": "Bob",
            },
        )

    assert response.status_code == 200
    assert response.json()["name"] == "Bob"
