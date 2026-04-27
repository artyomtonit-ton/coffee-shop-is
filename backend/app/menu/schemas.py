from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class CategoryBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: str | None = None


class CategoryCreate(CategoryBase):
    pass


class CategoryRead(CategoryBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class ProductBase(BaseModel):
    category_id: int
    name: str = Field(..., min_length=1, max_length=150)
    description: str | None = None
    price: Decimal = Field(..., gt=0, max_digits=10, decimal_places=2)
    image_url: str | None = Field(default=None, max_length=500)
    calories: int | None = Field(default=None, ge=0)
    weight: int | None = Field(default=None, ge=0)
    volume: int | None = Field(default=None, ge=0)
    is_available: bool = True
    is_preorder_available: bool = True


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    category_id: int | None = None
    name: str | None = Field(default=None, min_length=1, max_length=150)
    description: str | None = None
    price: Decimal | None = Field(default=None, gt=0, max_digits=10, decimal_places=2)
    image_url: str | None = Field(default=None, max_length=500)
    calories: int | None = Field(default=None, ge=0)
    weight: int | None = Field(default=None, ge=0)
    volume: int | None = Field(default=None, ge=0)
    is_available: bool | None = None
    is_preorder_available: bool | None = None


class ProductRead(ProductBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
