from decimal import Decimal

from fastapi import HTTPException, status

from app.loyalty.repository import LoyaltyRepository
from app.loyalty.service import LoyaltyService
from app.orders.models import Order
from app.orders.repository import OrderRepository, build_order_item
from app.orders.schemas import OrderCreate, OrderStatus, OrderStatusUpdate, OrderType
from app.users.models import User


class OrderService:
    def __init__(self, repository: OrderRepository):
        self.repository = repository

    def create_order(self, order_data: OrderCreate, user: User) -> Order:
        products_by_id = self._get_available_products(order_data)
        items = []
        total_amount = Decimal("0.00")

        for item_data in order_data.items:
            product = products_by_id[item_data.product_id]
            order_item = build_order_item(product, item_data.quantity)
            items.append(order_item)
            total_amount += order_item.total_price

        if order_data.bonus_used > total_amount:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Bonus amount cannot be greater than order total",
            )

        loyalty_service = LoyaltyService(LoyaltyRepository(self.repository.db))
        loyalty_service.validate_bonus_usage(user.id, order_data.bonus_used, total_amount)

        order = Order(
            user_id=user.id,
            status=OrderStatus.created.value,
            order_type=order_data.order_type.value,
            pickup_time=order_data.pickup_time,
            total_amount=total_amount,
            bonus_used=order_data.bonus_used,
            bonus_accrued=Decimal("0.00"),
            items=items,
        )
        created_order = self.repository.create_order(order)
        loyalty_service.write_off_for_order(
            user_id=user.id,
            order_id=created_order.id,
            amount=order_data.bonus_used,
            order_total=total_amount,
        )
        return self.repository.get_by_id(created_order.id) or created_order

    def get_user_orders(self, user: User) -> list[Order]:
        return self.repository.get_user_orders(user.id)

    def get_user_order(self, order_id: int, user: User) -> Order:
        order = self.repository.get_by_id(order_id)
        if order is None or order.user_id != user.id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Order not found",
            )
        return order

    def cancel_order(self, order_id: int, user: User) -> Order:
        order = self.get_user_order(order_id, user)
        if order.status in {OrderStatus.completed.value, OrderStatus.cancelled.value}:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Completed or cancelled orders cannot be cancelled",
            )

        return self.repository.update_status(order, OrderStatus.cancelled.value)

    def get_all_orders(self) -> list[Order]:
        return self.repository.get_all_orders()

    def update_order_status(
        self,
        order_id: int,
        status_data: OrderStatusUpdate,
    ) -> Order:
        order = self.repository.get_by_id(order_id)
        if order is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Order not found",
            )

        previous_status = order.status
        updated_order = self.repository.update_status(order, status_data.status.value)
        if (
            status_data.status == OrderStatus.completed
            and previous_status != OrderStatus.completed.value
        ):
            loyalty_service = LoyaltyService(LoyaltyRepository(self.repository.db))
            loyalty_service.accrue_for_completed_order(updated_order)
            return self.repository.get_by_id(updated_order.id) or updated_order

        return updated_order

    def _get_available_products(self, order_data: OrderCreate):
        product_ids = [item.product_id for item in order_data.items]
        if len(product_ids) != len(set(product_ids)):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Duplicate products are not allowed in one order",
            )

        products = self.repository.get_products_by_ids(product_ids)
        products_by_id = {product.id: product for product in products}
        missing_ids = sorted(set(product_ids) - set(products_by_id))
        if missing_ids:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Products not found: {missing_ids}",
            )

        unavailable_ids = [
            product.id
            for product in products
            if not product.is_available
            or (
                order_data.order_type == OrderType.preorder
                and not product.is_preorder_available
            )
        ]
        if unavailable_ids:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Products are not available: {sorted(unavailable_ids)}",
            )

        return products_by_id
