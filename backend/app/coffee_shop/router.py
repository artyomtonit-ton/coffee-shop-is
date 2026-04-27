from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.coffee_shop.repository import CoffeeShopRepository
from app.coffee_shop.schemas import CoffeeShopLocationRead, CoffeeShopRead
from app.coffee_shop.service import CoffeeShopService
from app.database import get_db


router = APIRouter(prefix="/coffee-shop", tags=["coffee-shop"])


def get_coffee_shop_service(db: Session = Depends(get_db)) -> CoffeeShopService:
    return CoffeeShopService(CoffeeShopRepository(db))


@router.get("/info", response_model=CoffeeShopRead)
def get_info(service: CoffeeShopService = Depends(get_coffee_shop_service)):
    return service.get_info()


@router.get("/location", response_model=CoffeeShopLocationRead)
def get_location(service: CoffeeShopService = Depends(get_coffee_shop_service)):
    return service.get_info()
