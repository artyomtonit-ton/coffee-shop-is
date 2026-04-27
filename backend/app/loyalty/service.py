from decimal import Decimal, ROUND_DOWN

from fastapi import HTTPException, status

from app.loyalty.models import BonusTransaction, LoyaltyCard
from app.loyalty.repository import LoyaltyRepository
from app.loyalty.schemas import BonusTransactionType
from app.orders.models import Order
from app.users.models import User


CASHBACK_PERCENT = Decimal("0.05")
MAX_BONUS_PAYMENT_PERCENT = Decimal("0.50")
MONEY_STEP = Decimal("0.01")


class LoyaltyService:
    def __init__(self, repository: LoyaltyRepository):
        self.repository = repository

    def get_card(self, user: User) -> LoyaltyCard:
        return self.repository.get_or_create_card(user.id)

    def get_transactions(self, user: User) -> list[BonusTransaction]:
        card = self.get_card(user)
        return self.repository.get_transactions(card.id)

    def ensure_user_card(self, user_id: int) -> LoyaltyCard:
        return self.repository.get_or_create_card(user_id)

    def validate_bonus_usage(
        self,
        user_id: int,
        bonus_used: Decimal,
        order_total: Decimal,
    ) -> LoyaltyCard:
        card = self.repository.get_or_create_card(user_id)
        bonus_used = self._normalize_money(bonus_used)
        max_allowed = self._normalize_money(order_total * MAX_BONUS_PAYMENT_PERCENT)

        if bonus_used > max_allowed:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Bonuses can cover no more than 50% of the order total",
            )

        if bonus_used > card.balance:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Not enough bonuses on loyalty card",
            )

        return card

    def write_off_for_order(
        self,
        user_id: int,
        order_id: int,
        amount: Decimal,
        order_total: Decimal,
    ) -> None:
        amount = self._normalize_money(amount)
        if amount <= 0:
            return

        card = self.validate_bonus_usage(user_id, amount, order_total)
        self.repository.update_card_balance(card, card.balance - amount)
        self.repository.add_transaction(
            card=card,
            transaction_type=BonusTransactionType.write_off.value,
            amount=amount,
            order_id=order_id,
            description="Payment with bonuses",
        )

    def accrue_for_completed_order(self, order: Order) -> Decimal:
        if order.bonus_accrued > 0:
            return order.bonus_accrued

        accrual_base = order.total_amount - order.bonus_used
        bonus_amount = self._normalize_money(accrual_base * CASHBACK_PERCENT)
        if bonus_amount <= 0:
            return Decimal("0.00")

        card = self.repository.get_or_create_card(order.user_id)
        self.repository.update_card_balance(card, card.balance + bonus_amount)
        order.bonus_accrued = bonus_amount
        self.repository.add_transaction(
            card=card,
            transaction_type=BonusTransactionType.accrual.value,
            amount=bonus_amount,
            order_id=order.id,
            description="Cashback for completed order",
        )
        return bonus_amount

    def add_bonus(
        self,
        user_id: int,
        amount: Decimal,
        order_id: int | None,
        description: str,
    ) -> None:
        amount = self._normalize_money(amount)
        if amount <= 0:
            return

        card = self.repository.get_or_create_card(user_id)
        self.repository.update_card_balance(card, card.balance + amount)
        self.repository.add_transaction(
            card=card,
            transaction_type=BonusTransactionType.accrual.value,
            amount=amount,
            order_id=order_id,
            description=description,
        )

    def _normalize_money(self, value: Decimal) -> Decimal:
        return value.quantize(MONEY_STEP, rounding=ROUND_DOWN)
