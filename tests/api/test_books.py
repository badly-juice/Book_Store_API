from app.api.deps import get_book_service
from app.core.dependencies import get_current_admin


def test_get_books(build_client) -> None:
    from tests.conftest import FakeBookService

    client = build_client(
        {
            get_book_service: lambda: FakeBookService(),
        }
    )

    with client:
        response = client.get("/api/v1/books/")

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["title"] == "The Pragmatic Book"
    assert data[0]["category_ids"]


def test_get_book(build_client) -> None:
    from uuid import uuid4

    from tests.conftest import FakeBookService

    book_id = uuid4()

    client = build_client(
        {
            get_book_service: lambda: FakeBookService(),
        }
    )

    with client:
        response = client.get(f"/api/v1/books/{book_id}")

    assert response.status_code == 200
    assert response.json()["id"] == str(book_id)


def test_create_book_requires_admin(build_client) -> None:
    from tests.conftest import FakeBookService

    client = build_client(
        {
            get_book_service: lambda: FakeBookService(),
        }
    )

    with client:
        response = client.post(
            "/api/v1/books/",
            json={
                "title": "Clean Architecture",
                "author": "Robert Martin",
                "description": "A book about software architecture.",
                "price": "29.99",
                "stock": 10,
                "isbn": "1234567890123",
                "category_ids": [],
            },
        )

    assert response.status_code in {401, 403}
