from datetime import UTC, datetime

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.orders.models import Order
from app.referrals.models import Referral
from app.users.models import User


class ReferralRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, inviter_id: int, invited_user_id: int) -> Referral:
        referral = Referral(inviter_id=inviter_id, invited_user_id=invited_user_id)
        self.db.add(referral)
        self.db.commit()
        self.db.refresh(referral)
        return referral

    def get_by_invited_user_id(self, invited_user_id: int) -> Referral | None:
        statement = select(Referral).where(Referral.invited_user_id == invited_user_id)
        return self.db.scalar(statement)

    def get_invited_users(self, inviter_id: int) -> list[tuple[Referral, User]]:
        statement = (
            select(Referral, User)
            .join(User, Referral.invited_user_id == User.id)
            .where(Referral.inviter_id == inviter_id)
            .order_by(Referral.created_at.desc(), Referral.id.desc())
        )
        return list(self.db.execute(statement).all())

    def count_completed_orders(self, user_id: int) -> int:
        statement = (
            select(func.count(Order.id))
            .where(Order.user_id == user_id, Order.status == "completed")
        )
        return self.db.scalar(statement) or 0

    def mark_bonus_awarded(self, referral: Referral) -> Referral:
        referral.bonus_awarded = True
        referral.bonus_awarded_at = datetime.now(UTC)
        self.db.flush()
        self.db.refresh(referral)
        return referral
