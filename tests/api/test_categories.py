from uuid import uuid4

from app.api.deps import get_category_service
from app.core.dependencies import get_current_admin


def test_get_categories(build_client) -> None:
    from tests.conftest import FakeCategoryService

    client = build_client(
        {
            get_category_service: lambda: FakeCategoryService(),
        }
    )

    with client:
        response = client.get("/api/v1/categories/")

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["name"] == "Programming"


def test_get_category(build_client) -> None:
    from tests.conftest import FakeCategoryService

    category_id = uuid4()

    client = build_client(
        {
            get_category_service: lambda: FakeCategoryService(),
        }
    )

    with client:
        response = client.get(f"/api/v1/categories/{category_id}")

    assert response.status_code == 200
    assert response.json()["id"] == str(category_id)


def test_create_category_requires_admin(build_client) -> None:
    from tests.conftest import FakeCategoryService

    client = build_client(
        {
            get_category_service: lambda: FakeCategoryService(),
        }
    )

    with client:
        response = client.post(
            "/api/v1/categories/",
            json={"name": "Programming"},
        )

    assert response.status_code in {401, 403}
