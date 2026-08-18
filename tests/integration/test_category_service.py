from uuid import uuid4

import pytest

from app.exceptions.all_exceptions import CategoryNotFoundError
from app.schemas.category import CategoryCreate, CategoryUpdate
from app.services.category import CategoryService


@pytest.mark.asyncio
async def test_create_category(session):
    service = CategoryService(session)

    category = await service.create_category(CategoryCreate(name="Programming"))

    assert category.id is not None
    assert category.name == "Programming"


@pytest.mark.asyncio
async def test_get_category(session):
    service = CategoryService(session)

    category = await service.create_category(CategoryCreate(name="Programming"))

    result = await service.get_category(category.id)

    assert result.id == category.id
    assert result.name == "Programming"


@pytest.mark.asyncio
async def test_update_category(session):
    service = CategoryService(session)

    category = await service.create_category(CategoryCreate(name="Programming"))

    updated = await service.update_category(
        category.id,
        CategoryUpdate(name="Python"),
    )

    assert updated.name == "Python"


@pytest.mark.asyncio
async def test_delete_category(session):
    service = CategoryService(session)

    category = await service.create_category(CategoryCreate(name="Programming"))

    await service.delete_category(category.id)

    with pytest.raises(CategoryNotFoundError):
        await service.get_category(category.id)


@pytest.mark.asyncio
async def test_get_missing_category_fails(session):
    service = CategoryService(session)

    with pytest.raises(CategoryNotFoundError):
        await service.get_category(uuid4())
