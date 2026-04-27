from datetime import datetime
from decimal import Decimal
from enum import Enum

from pydantic import BaseModel, ConfigDict


class BonusTransactionType(str, Enum):
    accrual = "accrual"
    write_off = "write_off"


class LoyaltyCardRead(BaseModel):
    id: int
    user_id: int
    balance: Decimal
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class BonusTransactionRead(BaseModel):
    id: int
    card_id: int
    order_id: int | None
    transaction_type: BonusTransactionType
    amount: Decimal
    description: str | None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
