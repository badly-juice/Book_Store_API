from uuid import UUID

from fastapi import APIRouter, status

from app.api.deps import BookServiceDep
from app.core.dependencies import CurrentAdminDep
from app.models.book import Book
from app.schemas.book import BookCreate, BookRead, BookUpdate

router = APIRouter(prefix="/books", tags=["Books"])


@router.get("/", response_model=list[BookRead])
async def get_books(service: BookServiceDep) -> list[Book]:
    return await service.get_books()


@router.get("/{book_id}", response_model=BookRead)
async def get_book(book_id: UUID, service: BookServiceDep) -> Book:
    return await service.get_book(book_id)


@router.post("/", response_model=BookRead, status_code=status.HTTP_201_CREATED)
async def create_book(
    book_data: BookCreate,
    service: BookServiceDep,
    _: CurrentAdminDep,
) -> Book:
    return await service.create_book(book_data)


@router.patch("/{book_id}", response_model=BookRead)
async def update_book(
    book_id: UUID,
    book_data: BookUpdate,
    service: BookServiceDep,
    _: CurrentAdminDep,
) -> Book:
    return await service.update_book(book_id, book_data)


@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(
    book_id: UUID,
    service: BookServiceDep,
    _: CurrentAdminDep,
) -> None:
    await service.delete_book(book_id)
