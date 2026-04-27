from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.common.dependencies import get_current_user
from app.database import get_db
from app.loyalty.repository import LoyaltyRepository
from app.loyalty.service import LoyaltyService
from app.referrals.repository import ReferralRepository
from app.referrals.schemas import InvitedUserRead, ReferralCodeApply, ReferralCodeRead
from app.referrals.service import ReferralService
from app.users.models import User
from app.users.repository import UserRepository


router = APIRouter(prefix="/referrals", tags=["referrals"])


def get_referral_service(db: Session = Depends(get_db)) -> ReferralService:
    return ReferralService(
        referral_repository=ReferralRepository(db),
        user_repository=UserRepository(db),
        loyalty_service=LoyaltyService(LoyaltyRepository(db)),
    )


@router.get("/my-code", response_model=ReferralCodeRead)
def get_my_code(
    current_user: User = Depends(get_current_user),
    service: ReferralService = Depends(get_referral_service),
):
    return ReferralCodeRead(referral_code=service.get_my_code(current_user))


@router.post("/apply-code", status_code=status.HTTP_201_CREATED)
def apply_code(
    code_data: ReferralCodeApply,
    current_user: User = Depends(get_current_user),
    service: ReferralService = Depends(get_referral_service),
):
    service.apply_code(current_user, code_data)
    return {"message": "Referral code applied"}


@router.get("/my-invited-users", response_model=list[InvitedUserRead])
def get_my_invited_users(
    current_user: User = Depends(get_current_user),
    service: ReferralService = Depends(get_referral_service),
):
    return service.get_my_invited_users(current_user)
