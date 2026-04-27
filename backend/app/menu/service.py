from fastapi import HTTPException, status

from app.menu.models import Category, Product
from app.menu.repository import MenuRepository
from app.menu.schemas import CategoryCreate, ProductCreate, ProductUpdate


class MenuService:
    def __init__(self, repository: MenuRepository):
        self.repository = repository

    def get_categories(self) -> list[Category]:
        return self.repository.get_categories()

    def create_category(self, category_data: CategoryCreate) -> Category:
        existing_category = self.repository.get_category_by_name(category_data.name)
        if existing_category:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Category with this name already exists",
            )

        return self.repository.create_category(category_data)

    def get_products(self) -> list[Product]:
        return self.repository.get_products(only_available=True)

    def get_product(self, product_id: int) -> Product:
        product = self.repository.get_product_by_id(product_id)
        if product is None or not product.is_available:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found",
            )

        return product

    def create_product(self, product_data: ProductCreate) -> Product:
        self._ensure_category_exists(product_data.category_id)
        return self.repository.create_product(product_data)

    def update_product(self, product_id: int, product_data: ProductUpdate) -> Product:
        product = self.repository.get_product_by_id(product_id)
        if product is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found",
            )

        if product_data.category_id is not None:
            self._ensure_category_exists(product_data.category_id)

        return self.repository.update_product(product, product_data)

    def delete_product(self, product_id: int) -> None:
        product = self.repository.get_product_by_id(product_id)
        if product is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found",
            )

        self.repository.delete_product(product)

    def _ensure_category_exists(self, category_id: int) -> None:
        category = self.repository.get_category_by_id(category_id)
        if category is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Category does not exist",
            )
