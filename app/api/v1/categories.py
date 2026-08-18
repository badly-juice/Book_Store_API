from uuid import UUID

from fastapi import APIRouter, status

from app.api.deps import CategoryServiceDep
from app.core.dependencies import CurrentAdminDep
from app.models.category import Category
from app.schemas.category import CategoryCreate, CategoryRead, CategoryUpdate

router = APIRouter(prefix="/categories", tags=["Categories"])


@router.get("/", response_model=list[CategoryRead])
async def get_categories(service: CategoryServiceDep) -> list[Category]:
    return await service.get_categories()


@router.get("/{category_id}", response_model=CategoryRead)
async def get_category(category_id: UUID, service: CategoryServiceDep) -> Category:
    return await service.get_category(category_id)


@router.post("/", response_model=CategoryRead, status_code=status.HTTP_201_CREATED)
async def create_category(
    category_data: CategoryCreate,
    service: CategoryServiceDep,
    _: CurrentAdminDep,
) -> Category:
    return await service.create_category(category_data)


@router.patch("/{category_id}", response_model=CategoryRead)
async def update_category(
    category_id: UUID,
    category_data: CategoryUpdate,
    service: CategoryServiceDep,
    _: CurrentAdminDep,
) -> Category:
    return await service.update_category(category_id, category_data)


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(
    category_id: UUID,
    service: CategoryServiceDep,
    _: CurrentAdminDep,
) -> None:
    await service.delete_category(category_id)
