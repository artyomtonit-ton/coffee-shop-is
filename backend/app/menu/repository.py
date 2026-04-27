from sqlalchemy import select
from sqlalchemy.orm import Session

from app.menu.models import Category, Product
from app.menu.schemas import CategoryCreate, ProductCreate, ProductUpdate


class MenuRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_categories(self) -> list[Category]:
        statement = select(Category).order_by(Category.name)
        return list(self.db.scalars(statement).all())

    def get_category_by_id(self, category_id: int) -> Category | None:
        return self.db.get(Category, category_id)

    def get_category_by_name(self, name: str) -> Category | None:
        statement = select(Category).where(Category.name == name)
        return self.db.scalar(statement)

    def create_category(self, category_data: CategoryCreate) -> Category:
        category = Category(**category_data.model_dump())
        self.db.add(category)
        self.db.commit()
        self.db.refresh(category)
        return category

    def get_products(self, only_available: bool = False) -> list[Product]:
        statement = select(Product).order_by(Product.name)
        if only_available:
            statement = statement.where(Product.is_available.is_(True))
        return list(self.db.scalars(statement).all())

    def get_product_by_id(self, product_id: int) -> Product | None:
        return self.db.get(Product, product_id)

    def create_product(self, product_data: ProductCreate) -> Product:
        product = Product(**product_data.model_dump())
        self.db.add(product)
        self.db.commit()
        self.db.refresh(product)
        return product

    def update_product(self, product: Product, product_data: ProductUpdate) -> Product:
        update_data = product_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(product, field, value)

        self.db.commit()
        self.db.refresh(product)
        return product

    def delete_product(self, product: Product) -> None:
        self.db.delete(product)
        self.db.commit()
