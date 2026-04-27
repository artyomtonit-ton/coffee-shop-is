from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.menu.repository import MenuRepository
from app.menu.schemas import CategoryRead, ProductRead
from app.menu.service import MenuService


router = APIRouter(prefix="/menu", tags=["menu"])


def get_menu_service(db: Session = Depends(get_db)) -> MenuService:
    return MenuService(MenuRepository(db))


@router.get("/categories", response_model=list[CategoryRead])
def get_categories(service: MenuService = Depends(get_menu_service)):
    return service.get_categories()


@router.get("/products", response_model=list[ProductRead])
def get_products(service: MenuService = Depends(get_menu_service)):
    return service.get_products()


@router.get("/products/{product_id}", response_model=ProductRead)
def get_product(product_id: int, service: MenuService = Depends(get_menu_service)):
    return service.get_product(product_id)
