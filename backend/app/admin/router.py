from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from app.coffee_shop.repository import CoffeeShopRepository
from app.coffee_shop.schemas import CoffeeShopRead, CoffeeShopUpdate
from app.coffee_shop.service import CoffeeShopService
from app.common.dependencies import get_current_admin_user
from app.database import get_db
from app.menu.repository import MenuRepository
from app.menu.schemas import (
    CategoryCreate,
    CategoryRead,
    ProductCreate,
    ProductRead,
    ProductUpdate,
)
from app.menu.service import MenuService
from app.orders.repository import OrderRepository
from app.orders.schemas import OrderRead, OrderStatusUpdate
from app.orders.service import OrderService
from app.promotions.repository import PromotionRepository
from app.promotions.schemas import PromotionCreate, PromotionRead, PromotionUpdate
from app.promotions.service import PromotionService


router = APIRouter(
    prefix="/admin",
    tags=["admin"],
    dependencies=[Depends(get_current_admin_user)],
)


def get_menu_service(db: Session = Depends(get_db)) -> MenuService:
    return MenuService(MenuRepository(db))


def get_order_service(db: Session = Depends(get_db)) -> OrderService:
    return OrderService(OrderRepository(db))


def get_promotion_service(db: Session = Depends(get_db)) -> PromotionService:
    return PromotionService(PromotionRepository(db))


def get_coffee_shop_service(db: Session = Depends(get_db)) -> CoffeeShopService:
    return CoffeeShopService(CoffeeShopRepository(db))


@router.post("/categories", response_model=CategoryRead, status_code=status.HTTP_201_CREATED)
def create_category(
    category_data: CategoryCreate,
    service: MenuService = Depends(get_menu_service),
):
    return service.create_category(category_data)


@router.post("/products", response_model=ProductRead, status_code=status.HTTP_201_CREATED)
def create_product(
    product_data: ProductCreate,
    service: MenuService = Depends(get_menu_service),
):
    return service.create_product(product_data)


@router.patch("/products/{product_id}", response_model=ProductRead)
def update_product(
    product_id: int,
    product_data: ProductUpdate,
    service: MenuService = Depends(get_menu_service),
):
    return service.update_product(product_id, product_data)


@router.delete("/products/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(
    product_id: int,
    service: MenuService = Depends(get_menu_service),
):
    service.delete_product(product_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get("/orders", response_model=list[OrderRead])
def get_orders(service: OrderService = Depends(get_order_service)):
    return service.get_all_orders()


@router.patch("/orders/{order_id}/status", response_model=OrderRead)
def update_order_status(
    order_id: int,
    status_data: OrderStatusUpdate,
    service: OrderService = Depends(get_order_service),
):
    return service.update_order_status(order_id, status_data)


@router.post("/promotions", response_model=PromotionRead, status_code=status.HTTP_201_CREATED)
def create_promotion(
    promotion_data: PromotionCreate,
    service: PromotionService = Depends(get_promotion_service),
):
    return service.create_promotion(promotion_data)


@router.patch("/promotions/{promotion_id}", response_model=PromotionRead)
def update_promotion(
    promotion_id: int,
    promotion_data: PromotionUpdate,
    service: PromotionService = Depends(get_promotion_service),
):
    return service.update_promotion(promotion_id, promotion_data)


@router.delete("/promotions/{promotion_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_promotion(
    promotion_id: int,
    service: PromotionService = Depends(get_promotion_service),
):
    service.delete_promotion(promotion_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.patch("/coffee-shop", response_model=CoffeeShopRead)
def update_coffee_shop(
    coffee_shop_data: CoffeeShopUpdate,
    service: CoffeeShopService = Depends(get_coffee_shop_service),
):
    return service.update_info(coffee_shop_data)
