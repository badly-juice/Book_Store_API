from uuid import UUID

from fastapi import APIRouter, status

from app.api.deps import OrderServiceDep
from app.core.dependencies import CurrentUserDep
from app.models.order import Order
from app.schemas.order import OrderCreate, OrderRead
from app.schemas.order_item import OrderItemCreate

router = APIRouter(prefix="/orders", tags=["Orders"])


@router.get("/", response_model=list[OrderRead])
async def get_orders(service: OrderServiceDep, current_user: CurrentUserDep) -> list[Order]:
    return await service.get_orders(current_user)


@router.get("/{order_id}", response_model=OrderRead)
async def get_order(
    order_id: UUID,
    service: OrderServiceDep,
    current_user: CurrentUserDep,
) -> Order:
    return await service.get_order(order_id, current_user)


@router.post("/", response_model=OrderRead, status_code=status.HTTP_201_CREATED)
async def create_order(service: OrderServiceDep, current_user: CurrentUserDep) -> Order:
    return await service.create_order(current_user)


@router.post("/{order_id}/items", response_model=OrderRead)
async def add_item(
    order_id: UUID,
    item_data: OrderItemCreate,
    service: OrderServiceDep,
    current_user: CurrentUserDep,
) -> Order:
    return await service.add_item(order_id, item_data, current_user)


@router.post("/{order_id}/cancel", response_model=OrderRead)
async def cancel_order(
    order_id: UUID,
    service: OrderServiceDep,
    current_user: CurrentUserDep,
) -> Order:
    return await service.cancel_order(order_id, current_user)
