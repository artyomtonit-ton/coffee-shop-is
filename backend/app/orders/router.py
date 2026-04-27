from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.common.dependencies import get_current_user
from app.database import get_db
from app.orders.repository import OrderRepository
from app.orders.schemas import OrderCreate, OrderRead
from app.orders.service import OrderService
from app.users.models import User


router = APIRouter(prefix="/orders", tags=["orders"])


def get_order_service(db: Session = Depends(get_db)) -> OrderService:
    return OrderService(OrderRepository(db))


@router.post("", response_model=OrderRead, status_code=status.HTTP_201_CREATED)
def create_order(
    order_data: OrderCreate,
    current_user: User = Depends(get_current_user),
    service: OrderService = Depends(get_order_service),
):
    return service.create_order(order_data, current_user)


@router.get("/my", response_model=list[OrderRead])
def get_my_orders(
    current_user: User = Depends(get_current_user),
    service: OrderService = Depends(get_order_service),
):
    return service.get_user_orders(current_user)


@router.get("/{order_id}", response_model=OrderRead)
def get_order(
    order_id: int,
    current_user: User = Depends(get_current_user),
    service: OrderService = Depends(get_order_service),
):
    return service.get_user_order(order_id, current_user)


@router.patch("/{order_id}/cancel", response_model=OrderRead)
def cancel_order(
    order_id: int,
    current_user: User = Depends(get_current_user),
    service: OrderService = Depends(get_order_service),
):
    return service.cancel_order(order_id, current_user)
