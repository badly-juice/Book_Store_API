from uuid import uuid4

from app.api.deps import get_order_service
from app.core.dependencies import get_current_user


def test_create_order(build_client, user) -> None:
    from tests.conftest import FakeOrderService

    client = build_client(
        {
            get_current_user: lambda: user,
            get_order_service: lambda: FakeOrderService(),
        }
    )

    with client:
        response = client.post("/api/v1/orders/")

    assert response.status_code == 201

    data = response.json()

    assert data["user_id"] == str(user.id)
    assert data["status"] == "pending"
    assert data["total_price"] == "0"
    assert data["order_items"] == []


def test_openapi_exposes_core_routes(build_client) -> None:
    client = build_client({})

    with client:
        paths = client.app.openapi()["paths"]

    assert "/api/v1/auth/login" in paths
    assert "/api/v1/users/me" in paths
    assert "/api/v1/books/" in paths
    assert "/api/v1/categories/" in paths
    assert "/api/v1/orders/" in paths
    assert "/api/v1/orders/{order_id}/items" in paths
    assert "/api/v1/orders/{order_id}/cancel" in paths


# def test_add_item_to_order(build_client, user) -> None:
#     from tests.conftest import FakeOrderService
#
#     client = build_client(
#         {
#             get_current_user: lambda: user,
#             get_order_service: lambda: FakeOrderService(),
#         }
#     )
#
#     order_id = uuid4()
#     book_id = uuid4()
#
#     with client:
#         response = client.post(
#             f"/api/v1/orders/{order_id}/items",
#             json={
#                 "book_id": str(book_id),
#                 "quantity": 2,
#             },
#         )
#
#
#     assert response.status_code == 200
