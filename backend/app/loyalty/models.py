from datetime import datetime
from decimal import Decimal

from sqlalchemy import DateTime, ForeignKey, Numeric, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class LoyaltyCard(Base):
    __tablename__ = "loyalty_cards"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        unique=True,
        index=True,
        nullable=False,
    )
    balance: Mapped[Decimal] = mapped_column(Numeric(10, 2), default=0, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    transactions: Mapped[list["BonusTransaction"]] = relationship(
        back_populates="card",
        cascade="all, delete-orphan",
    )


class BonusTransaction(Base):
    __tablename__ = "bonus_transactions"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    card_id: Mapped[int] = mapped_column(
        ForeignKey("loyalty_cards.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    order_id: Mapped[int | None] = mapped_column(ForeignKey("orders.id"), index=True, nullable=True)
    transaction_type: Mapped[str] = mapped_column(String(30), nullable=False)
    amount: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    description: Mapped[str | None] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    card: Mapped[LoyaltyCard] = relationship(back_populates="transactions")
