from __future__ import annotations

import sys
from datetime import date, timedelta
from decimal import Decimal
from pathlib import Path

from sqlalchemy import select
from sqlalchemy.orm import Session


BACKEND_DIR = Path(__file__).resolve().parents[1]
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from app.coffee_shop.models import CoffeeShop
from app.common.security import get_password_hash
from app.database import SessionLocal
from app.loyalty.models import LoyaltyCard
from app.menu.models import Category, Product
from app.promotions.models import Promotion
from app.users.models import Profile, Role, User


ADMIN_EMAIL = "admin@coffee-shop.local"
ADMIN_PASSWORD = "Admin12345"
USER_EMAIL = "user@coffee-shop.local"
USER_PASSWORD = "User12345"


def get_or_create_role(db: Session, name: str) -> Role:
    role = db.scalar(select(Role).where(Role.name == name))
    if role is not None:
        return role

    role = Role(name=name)
    db.add(role)
    db.flush()
    return role


def upsert_user(
    db: Session,
    *,
    email: str,
    password: str,
    role: Role,
    referral_code: str,
    first_name: str,
    last_name: str,
    phone: str,
) -> User:
    user = db.scalar(select(User).where(User.email == email))
    if user is None:
        user = User(
            email=email,
            hashed_password=get_password_hash(password),
            referral_code=referral_code,
            role_id=role.id,
            is_active=True,
        )
        db.add(user)
        db.flush()
    else:
        user.hashed_password = get_password_hash(password)
        user.referral_code = referral_code
        user.role_id = role.id
        user.is_active = True

    if user.profile is None:
        user.profile = Profile(
            first_name=first_name,
            last_name=last_name,
            phone=phone,
        )
    else:
        user.profile.first_name = first_name
        user.profile.last_name = last_name
        user.profile.phone = phone

    loyalty_card = db.scalar(
        select(LoyaltyCard).where(LoyaltyCard.user_id == user.id),
    )
    if loyalty_card is None:
        db.add(LoyaltyCard(user_id=user.id, balance=Decimal("250.00")))
    elif email == USER_EMAIL:
        loyalty_card.balance = Decimal("250.00")

    return user


def upsert_category(db: Session, name: str, description: str) -> Category:
    category = db.scalar(select(Category).where(Category.name == name))
    if category is None:
        category = Category(name=name, description=description)
        db.add(category)
        db.flush()
    else:
        category.description = description
    return category


def upsert_product(
    db: Session,
    *,
    category: Category,
    name: str,
    description: str,
    price: str,
    calories: int | None,
    weight: int | None,
    volume: int | None,
    image_url: str,
    is_available: bool = True,
    is_preorder_available: bool = True,
) -> Product:
    product = db.scalar(select(Product).where(Product.name == name))
    if product is None:
        product = Product(name=name)
        db.add(product)

    product.category_id = category.id
    product.description = description
    product.price = Decimal(price)
    product.calories = calories
    product.weight = weight
    product.volume = volume
    product.image_url = image_url
    product.is_available = is_available
    product.is_preorder_available = is_preorder_available
    return product


def upsert_promotion(
    db: Session,
    *,
    title: str,
    description: str,
    discount_percent: int,
    start_date: date,
    end_date: date,
    is_active: bool = True,
) -> Promotion:
    promotion = db.scalar(select(Promotion).where(Promotion.title == title))
    if promotion is None:
        promotion = Promotion(title=title)
        db.add(promotion)

    promotion.description = description
    promotion.discount_percent = discount_percent
    promotion.start_date = start_date
    promotion.end_date = end_date
    promotion.is_active = is_active
    return promotion


def upsert_coffee_shop(db: Session) -> CoffeeShop:
    coffee_shop = db.scalar(select(CoffeeShop).order_by(CoffeeShop.id).limit(1))
    if coffee_shop is None:
        coffee_shop = CoffeeShop(
            name="Brew & Study Coffee",
            address="Moscow, Tverskaya Street, 15",
        )
        db.add(coffee_shop)

    coffee_shop.name = "Brew & Study Coffee"
    coffee_shop.address = "Moscow, Tverskaya Street, 15"
    coffee_shop.latitude = Decimal("55.761244")
    coffee_shop.longitude = Decimal("37.609425")
    coffee_shop.phone = "+7 999 123-45-67"
    coffee_shop.working_hours = "Mon-Fri 08:00-22:00, Sat-Sun 09:00-23:00"
    coffee_shop.description = (
        "Demo coffee shop for the diploma information system. "
        "Guests can view the menu, make pre-orders, use bonuses and promotions."
    )
    coffee_shop.image_url = "https://images.unsplash.com/photo-1501339847302-ac426a4a7cbb"
    coffee_shop.social_links = {
        "instagram": "https://instagram.com/brew-study-demo",
        "telegram": "https://t.me/brew_study_demo",
    }
    return coffee_shop


def seed_demo_data() -> None:
    today = date.today()

    with SessionLocal() as db:
        admin_role = get_or_create_role(db, "admin")
        user_role = get_or_create_role(db, "user")

        upsert_user(
            db,
            email=ADMIN_EMAIL,
            password=ADMIN_PASSWORD,
            role=admin_role,
            referral_code="ADMIN001",
            first_name="Admin",
            last_name="Coffee",
            phone="+7 999 000-00-01",
        )
        upsert_user(
            db,
            email=USER_EMAIL,
            password=USER_PASSWORD,
            role=user_role,
            referral_code="USER0001",
            first_name="Demo",
            last_name="Guest",
            phone="+7 999 000-00-02",
        )

        coffee = upsert_category(
            db,
            "Coffee",
            "Classic espresso drinks and milk-based coffee.",
        )
        tea = upsert_category(
            db,
            "Tea",
            "Black, green and herbal tea drinks.",
        )
        desserts = upsert_category(
            db,
            "Desserts",
            "Sweet bakery items for coffee orders.",
        )
        snacks = upsert_category(
            db,
            "Snacks",
            "Light food for breakfast and lunch.",
        )

        products = [
            {
                "category": coffee,
                "name": "Espresso",
                "description": "Rich classic espresso shot.",
                "price": "160.00",
                "calories": 5,
                "weight": None,
                "volume": 40,
                "image_url": "https://images.unsplash.com/photo-1510707577719-ae7c14805e3a",
            },
            {
                "category": coffee,
                "name": "Cappuccino",
                "description": "Espresso with steamed milk and dense foam.",
                "price": "240.00",
                "calories": 120,
                "weight": None,
                "volume": 250,
                "image_url": "https://images.unsplash.com/photo-1534778101976-62847782c213",
            },
            {
                "category": coffee,
                "name": "Latte",
                "description": "Soft milk coffee with a mild espresso taste.",
                "price": "260.00",
                "calories": 150,
                "weight": None,
                "volume": 300,
                "image_url": "https://images.unsplash.com/photo-1461023058943-07fcbe16d735",
            },
            {
                "category": coffee,
                "name": "Raf Coffee",
                "description": "Creamy coffee with vanilla sugar.",
                "price": "310.00",
                "calories": 210,
                "weight": None,
                "volume": 300,
                "image_url": "https://images.unsplash.com/photo-1495474472287-4d71bcdd2085",
            },
            {
                "category": tea,
                "name": "Green Tea",
                "description": "Fresh green tea with a light herbal aroma.",
                "price": "190.00",
                "calories": 2,
                "weight": None,
                "volume": 350,
                "image_url": "https://images.unsplash.com/photo-1544787219-7f47ccb76574",
            },
            {
                "category": tea,
                "name": "Berry Tea",
                "description": "Hot berry drink with black tea base.",
                "price": "230.00",
                "calories": 80,
                "weight": None,
                "volume": 400,
                "image_url": "https://images.unsplash.com/photo-1576092768241-dec231879fc3",
            },
            {
                "category": desserts,
                "name": "Cheesecake",
                "description": "Classic creamy cheesecake slice.",
                "price": "290.00",
                "calories": 320,
                "weight": 140,
                "volume": None,
                "image_url": "https://images.unsplash.com/photo-1533134242443-d4fd215305ad",
            },
            {
                "category": desserts,
                "name": "Chocolate Muffin",
                "description": "Soft chocolate muffin with cocoa chips.",
                "price": "180.00",
                "calories": 280,
                "weight": 110,
                "volume": None,
                "image_url": "https://images.unsplash.com/photo-1607958996333-41aef7caefaa",
            },
            {
                "category": snacks,
                "name": "Turkey Sandwich",
                "description": "Sandwich with turkey, cheese and fresh vegetables.",
                "price": "350.00",
                "calories": 410,
                "weight": 220,
                "volume": None,
                "image_url": "https://images.unsplash.com/photo-1528735602780-2552fd46c7af",
            },
            {
                "category": snacks,
                "name": "Croissant",
                "description": "Butter croissant baked until golden.",
                "price": "170.00",
                "calories": 260,
                "weight": 90,
                "volume": None,
                "image_url": "https://images.unsplash.com/photo-1555507036-ab1f4038808a",
            },
        ]
        for product_data in products:
            upsert_product(db, **product_data)

        upsert_promotion(
            db,
            title="Morning Coffee Set",
            description="10% discount for any coffee and dessert before noon.",
            discount_percent=10,
            start_date=today - timedelta(days=7),
            end_date=today + timedelta(days=30),
        )
        upsert_promotion(
            db,
            title="Student Week",
            description="15% discount for students on weekdays.",
            discount_percent=15,
            start_date=today - timedelta(days=3),
            end_date=today + timedelta(days=14),
        )
        upsert_promotion(
            db,
            title="Second Tea For A Friend",
            description="20% discount on the second tea drink in one order.",
            discount_percent=20,
            start_date=today,
            end_date=today + timedelta(days=21),
        )

        upsert_coffee_shop(db)

        db.commit()

    print("Demo seed data has been loaded successfully.")
    print(f"Admin account: {ADMIN_EMAIL} / {ADMIN_PASSWORD}")
    print(f"User account:  {USER_EMAIL} / {USER_PASSWORD}")


if __name__ == "__main__":
    seed_demo_data()
