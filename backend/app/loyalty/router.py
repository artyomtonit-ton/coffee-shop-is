from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.common.dependencies import get_current_user
from app.database import get_db
from app.loyalty.repository import LoyaltyRepository
from app.loyalty.schemas import BonusTransactionRead, LoyaltyCardRead
from app.loyalty.service import LoyaltyService
from app.users.models import User


router = APIRouter(prefix="/loyalty", tags=["loyalty"])


def get_loyalty_service(db: Session = Depends(get_db)) -> LoyaltyService:
    return LoyaltyService(LoyaltyRepository(db))


@router.get("/card", response_model=LoyaltyCardRead)
def get_card(
    current_user: User = Depends(get_current_user),
    service: LoyaltyService = Depends(get_loyalty_service),
):
    return service.get_card(current_user)


@router.get("/transactions", response_model=list[BonusTransactionRead])
def get_transactions(
    current_user: User = Depends(get_current_user),
    service: LoyaltyService = Depends(get_loyalty_service),
):
    return service.get_transactions(current_user)
