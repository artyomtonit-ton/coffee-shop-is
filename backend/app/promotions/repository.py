from datetime import date

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.promotions.models import Promotion
from app.promotions.schemas import PromotionCreate, PromotionUpdate


class PromotionRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_active_promotions(self, current_date: date) -> list[Promotion]:
        statement = (
            select(Promotion)
            .where(
                Promotion.is_active.is_(True),
                Promotion.start_date <= current_date,
                Promotion.end_date >= current_date,
            )
            .order_by(Promotion.created_at.desc(), Promotion.id.desc())
        )
        return list(self.db.scalars(statement).all())

    def get_by_id(self, promotion_id: int) -> Promotion | None:
        return self.db.get(Promotion, promotion_id)

    def create(self, promotion_data: PromotionCreate) -> Promotion:
        promotion = Promotion(**promotion_data.model_dump())
        self.db.add(promotion)
        self.db.commit()
        self.db.refresh(promotion)
        return promotion

    def update(self, promotion: Promotion, promotion_data: PromotionUpdate) -> Promotion:
        update_data = promotion_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(promotion, field, value)

        self.db.commit()
        self.db.refresh(promotion)
        return promotion

    def delete(self, promotion: Promotion) -> None:
        self.db.delete(promotion)
        self.db.commit()
