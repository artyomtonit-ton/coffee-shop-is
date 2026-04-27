from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.menu.models import Product
from app.orders.models import Order, OrderItem


class OrderRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_products_by_ids(self, product_ids: list[int]) -> list[Product]:
        statement = select(Product).where(Product.id.in_(product_ids))
        return list(self.db.scalars(statement).all())

    def create_order(self, order: Order) -> Order:
        self.db.add(order)
        self.db.commit()
        self.db.refresh(order)
        return self.get_by_id(order.id) or order

    def get_by_id(self, order_id: int) -> Order | None:
        statement = (
            select(Order)
            .options(selectinload(Order.items))
            .where(Order.id == order_id)
        )
        return self.db.scalar(statement)

    def get_user_orders(self, user_id: int) -> list[Order]:
        statement = (
            select(Order)
            .options(selectinload(Order.items))
            .where(Order.user_id == user_id)
            .order_by(Order.created_at.desc(), Order.id.desc())
        )
        return list(self.db.scalars(statement).all())

    def get_all_orders(self) -> list[Order]:
        statement = (
            select(Order)
            .options(selectinload(Order.items))
            .order_by(Order.created_at.desc(), Order.id.desc())
        )
        return list(self.db.scalars(statement).all())

    def update_status(self, order: Order, status: str) -> Order:
        order.status = status
        self.db.commit()
        self.db.refresh(order)
        return self.get_by_id(order.id) or order


def build_order_item(
    product: Product,
    quantity: int,
) -> OrderItem:
    unit_price = product.price
    total_price = unit_price * quantity
    return OrderItem(
        product_id=product.id,
        product_name=product.name,
        quantity=quantity,
        unit_price=unit_price,
        total_price=total_price,
    )
