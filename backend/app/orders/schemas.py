from datetime import datetime
from decimal import Decimal
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field


class OrderStatus(str, Enum):
    created = "created"
    accepted = "accepted"
    preparing = "preparing"
    ready = "ready"
    completed = "completed"
    cancelled = "cancelled"


class OrderType(str, Enum):
    offline = "offline"
    preorder = "preorder"


class OrderItemCreate(BaseModel):
    product_id: int
    quantity: int = Field(..., ge=1)


class OrderCreate(BaseModel):
    order_type: OrderType = OrderType.preorder
    pickup_time: datetime | None = None
    bonus_used: Decimal = Field(default=Decimal("0.00"), ge=0, max_digits=10, decimal_places=2)
    items: list[OrderItemCreate] = Field(..., min_length=1)


class OrderItemRead(BaseModel):
    id: int
    product_id: int
    product_name: str
    quantity: int
    unit_price: Decimal
    total_price: Decimal

    model_config = ConfigDict(from_attributes=True)


class OrderRead(BaseModel):
    id: int
    user_id: int
    status: OrderStatus
    order_type: OrderType
    total_amount: Decimal
    bonus_used: Decimal
    bonus_accrued: Decimal
    pickup_time: datetime | None
    created_at: datetime
    items: list[OrderItemRead]

    model_config = ConfigDict(from_attributes=True)


class OrderStatusUpdate(BaseModel):
    status: OrderStatus
