from sqlalchemy import select
from sqlalchemy.orm import Session

from app.coffee_shop.models import CoffeeShop
from app.coffee_shop.schemas import CoffeeShopUpdate


class CoffeeShopRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_info(self) -> CoffeeShop | None:
        statement = select(CoffeeShop).order_by(CoffeeShop.id).limit(1)
        return self.db.scalar(statement)

    def create(self, coffee_shop_data: CoffeeShopUpdate) -> CoffeeShop:
        data = coffee_shop_data.model_dump(exclude_unset=True)
        coffee_shop = CoffeeShop(
            name=data.pop("name", "Coffee Shop"),
            address=data.pop("address", "Address is not specified"),
            **data,
        )
        self.db.add(coffee_shop)
        self.db.commit()
        self.db.refresh(coffee_shop)
        return coffee_shop

    def update(
        self,
        coffee_shop: CoffeeShop,
        coffee_shop_data: CoffeeShopUpdate,
    ) -> CoffeeShop:
        update_data = coffee_shop_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(coffee_shop, field, value)

        self.db.commit()
        self.db.refresh(coffee_shop)
        return coffee_shop
