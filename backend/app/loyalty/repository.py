from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.loyalty.models import BonusTransaction, LoyaltyCard


class LoyaltyRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_card_by_user_id(self, user_id: int) -> LoyaltyCard | None:
        statement = select(LoyaltyCard).where(LoyaltyCard.user_id == user_id)
        return self.db.scalar(statement)

    def get_or_create_card(self, user_id: int) -> LoyaltyCard:
        card = self.get_card_by_user_id(user_id)
        if card is not None:
            return card

        card = LoyaltyCard(user_id=user_id, balance=Decimal("0.00"))
        self.db.add(card)
        self.db.commit()
        self.db.refresh(card)
        return card

    def get_transactions(self, card_id: int) -> list[BonusTransaction]:
        statement = (
            select(BonusTransaction)
            .where(BonusTransaction.card_id == card_id)
            .order_by(BonusTransaction.created_at.desc(), BonusTransaction.id.desc())
        )
        return list(self.db.scalars(statement).all())

    def add_transaction(
        self,
        card: LoyaltyCard,
        transaction_type: str,
        amount: Decimal,
        order_id: int | None,
        description: str,
    ) -> BonusTransaction:
        transaction = BonusTransaction(
            card_id=card.id,
            order_id=order_id,
            transaction_type=transaction_type,
            amount=amount,
            description=description,
        )
        self.db.add(transaction)
        self.db.flush()
        self.db.refresh(transaction)
        self.db.refresh(card)
        return transaction

    def update_card_balance(self, card: LoyaltyCard, balance: Decimal) -> LoyaltyCard:
        card.balance = balance
        self.db.add(card)
        return card
