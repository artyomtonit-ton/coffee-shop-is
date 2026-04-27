from fastapi import HTTPException, status

from app.coffee_shop.models import CoffeeShop
from app.coffee_shop.repository import CoffeeShopRepository
from app.coffee_shop.schemas import CoffeeShopUpdate


class CoffeeShopService:
    def __init__(self, repository: CoffeeShopRepository):
        self.repository = repository

    def get_info(self) -> CoffeeShop:
        coffee_shop = self.repository.get_info()
        if coffee_shop is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Coffee shop information is not configured",
            )
        return coffee_shop

    def update_info(self, coffee_shop_data: CoffeeShopUpdate) -> CoffeeShop:
        coffee_shop = self.repository.get_info()
        if coffee_shop is None:
            return self.repository.create(coffee_shop_data)

        return self.repository.update(coffee_shop, coffee_shop_data)
