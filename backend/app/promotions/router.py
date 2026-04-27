from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.promotions.repository import PromotionRepository
from app.promotions.schemas import PromotionRead
from app.promotions.service import PromotionService


router = APIRouter(prefix="/promotions", tags=["promotions"])


def get_promotion_service(db: Session = Depends(get_db)) -> PromotionService:
    return PromotionService(PromotionRepository(db))


@router.get("", response_model=list[PromotionRead])
def get_promotions(service: PromotionService = Depends(get_promotion_service)):
    return service.get_active_promotions()


@router.get("/{promotion_id}", response_model=PromotionRead)
def get_promotion(
    promotion_id: int,
    service: PromotionService = Depends(get_promotion_service),
):
    return service.get_active_promotion(promotion_id)
