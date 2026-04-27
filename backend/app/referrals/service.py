from decimal import Decimal

from fastapi import HTTPException, status

from app.loyalty.service import LoyaltyService
from app.orders.models import Order
from app.referrals.models import Referral
from app.referrals.repository import ReferralRepository
from app.referrals.schemas import InvitedUserRead, ReferralCodeApply
from app.users.models import User
from app.users.repository import UserRepository
from app.users.service import UserService


INVITER_REFERRAL_BONUS = Decimal("100.00")
INVITED_REFERRAL_BONUS = Decimal("50.00")


class ReferralService:
    def __init__(
        self,
        referral_repository: ReferralRepository,
        user_repository: UserRepository,
        loyalty_service: LoyaltyService | None = None,
    ):
        self.referral_repository = referral_repository
        self.user_repository = user_repository
        self.loyalty_service = loyalty_service

    def get_my_code(self, user: User) -> str:
        return UserService(self.user_repository).ensure_referral_code(user)

    def apply_code(self, user: User, code_data: ReferralCodeApply) -> Referral:
        self.get_my_code(user)

        existing_referral = self.referral_repository.get_by_invited_user_id(user.id)
        if existing_referral is not None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Referral code has already been applied",
            )

        inviter = self.user_repository.get_by_referral_code(code_data.referral_code)
        if inviter is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Referral code not found",
            )

        if inviter.id == user.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="You cannot use your own referral code",
            )

        return self.referral_repository.create(
            inviter_id=inviter.id,
            invited_user_id=user.id,
        )

    def get_my_invited_users(self, user: User) -> list[InvitedUserRead]:
        rows = self.referral_repository.get_invited_users(user.id)
        return [
            InvitedUserRead(
                referral_id=referral.id,
                invited_user_id=invited_user.id,
                invited_user_email=invited_user.email,
                bonus_awarded=referral.bonus_awarded,
                created_at=referral.created_at,
            )
            for referral, invited_user in rows
        ]

    def process_first_completed_order_bonus(self, order: Order) -> None:
        if self.loyalty_service is None:
            raise RuntimeError("Loyalty service is required")

        referral = self.referral_repository.get_by_invited_user_id(order.user_id)
        if referral is None or referral.bonus_awarded:
            return

        completed_orders_count = self.referral_repository.count_completed_orders(order.user_id)
        if completed_orders_count != 1:
            return

        self.loyalty_service.add_bonus(
            user_id=referral.inviter_id,
            amount=INVITER_REFERRAL_BONUS,
            order_id=order.id,
            description="Referral bonus for invited user's first completed order",
        )
        self.loyalty_service.add_bonus(
            user_id=referral.invited_user_id,
            amount=INVITED_REFERRAL_BONUS,
            order_id=order.id,
            description="Referral bonus for first completed order",
        )
        self.referral_repository.mark_bonus_awarded(referral)
