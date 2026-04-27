from datetime import date

from fastapi import HTTPException, status

from app.promotions.models import Promotion
from app.promotions.repository import PromotionRepository
from app.promotions.schemas import PromotionCreate, PromotionUpdate


class PromotionService:
    def __init__(self, repository: PromotionRepository):
        self.repository = repository

    def get_active_promotions(self) -> list[Promotion]:
        return self.repository.get_active_promotions(date.today())

    def get_active_promotion(self, promotion_id: int) -> Promotion:
        promotion = self.repository.get_by_id(promotion_id)
        today = date.today()
        if (
            promotion is None
            or not promotion.is_active
            or promotion.start_date > today
            or promotion.end_date < today
        ):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Promotion not found",
            )
        return promotion

    def create_promotion(self, promotion_data: PromotionCreate) -> Promotion:
        return self.repository.create(promotion_data)

    def update_promotion(
        self,
        promotion_id: int,
        promotion_data: PromotionUpdate,
    ) -> Promotion:
        promotion = self._get_promotion_or_404(promotion_id)

        start_date = promotion_data.start_date or promotion.start_date
        end_date = promotion_data.end_date or promotion.end_date
        if end_date < start_date:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="end_date must be greater than or equal to start_date",
            )

        return self.repository.update(promotion, promotion_data)

    def delete_promotion(self, promotion_id: int) -> None:
        promotion = self._get_promotion_or_404(promotion_id)
        self.repository.delete(promotion)

    def _get_promotion_or_404(self, promotion_id: int) -> Promotion:
        promotion = self.repository.get_by_id(promotion_id)
        if promotion is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Promotion not found",
            )
        return promotion
