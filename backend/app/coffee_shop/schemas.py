from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class CoffeeShopBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=150)
    address: str = Field(..., min_length=1, max_length=255)
    latitude: Decimal | None = Field(default=None, ge=-90, le=90)
    longitude: Decimal | None = Field(default=None, ge=-180, le=180)
    phone: str | None = Field(default=None, max_length=30)
    working_hours: str | None = Field(default=None, max_length=255)
    description: str | None = None
    image_url: str | None = Field(default=None, max_length=500)
    social_links: dict[str, str] | None = None


class CoffeeShopUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=150)
    address: str | None = Field(default=None, min_length=1, max_length=255)
    latitude: Decimal | None = Field(default=None, ge=-90, le=90)
    longitude: Decimal | None = Field(default=None, ge=-180, le=180)
    phone: str | None = Field(default=None, max_length=30)
    working_hours: str | None = Field(default=None, max_length=255)
    description: str | None = None
    image_url: str | None = Field(default=None, max_length=500)
    social_links: dict[str, str] | None = None


class CoffeeShopRead(CoffeeShopBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class CoffeeShopLocationRead(BaseModel):
    name: str
    address: str
    latitude: Decimal | None
    longitude: Decimal | None
    phone: str | None
    working_hours: str | None

    model_config = ConfigDict(from_attributes=True)
