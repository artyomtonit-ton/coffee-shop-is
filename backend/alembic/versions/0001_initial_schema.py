"""initial schema

Revision ID: 0001_initial_schema
Revises:
Create Date: 2026-04-28 02:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "0001_initial_schema"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "categories",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_categories_id"), "categories", ["id"], unique=False)
    op.create_index(op.f("ix_categories_name"), "categories", ["name"], unique=True)

    op.create_table(
        "coffee_shops",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=150), nullable=False),
        sa.Column("address", sa.String(length=255), nullable=False),
        sa.Column("latitude", sa.Numeric(9, 6), nullable=True),
        sa.Column("longitude", sa.Numeric(9, 6), nullable=True),
        sa.Column("phone", sa.String(length=30), nullable=True),
        sa.Column("working_hours", sa.String(length=255), nullable=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("image_url", sa.String(length=500), nullable=True),
        sa.Column("social_links", sa.JSON(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_coffee_shops_id"), "coffee_shops", ["id"], unique=False)

    op.create_table(
        "promotions",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(length=150), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("discount_percent", sa.Integer(), nullable=False),
        sa.Column("start_date", sa.Date(), nullable=False),
        sa.Column("end_date", sa.Date(), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_promotions_id"), "promotions", ["id"], unique=False)

    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("hashed_password", sa.String(length=255), nullable=False),
        sa.Column("referral_code", sa.String(length=20), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_users_email"), "users", ["email"], unique=True)
    op.create_index(op.f("ix_users_id"), "users", ["id"], unique=False)
    op.create_index(op.f("ix_users_referral_code"), "users", ["referral_code"], unique=True)

    op.create_table(
        "loyalty_cards",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("balance", sa.Numeric(10, 2), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_loyalty_cards_id"), "loyalty_cards", ["id"], unique=False)
    op.create_index(op.f("ix_loyalty_cards_user_id"), "loyalty_cards", ["user_id"], unique=True)

    op.create_table(
        "orders",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("status", sa.String(length=30), nullable=False),
        sa.Column("order_type", sa.String(length=30), nullable=False),
        sa.Column("total_amount", sa.Numeric(10, 2), nullable=False),
        sa.Column("bonus_used", sa.Numeric(10, 2), nullable=False),
        sa.Column("bonus_accrued", sa.Numeric(10, 2), nullable=False),
        sa.Column("pickup_time", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_orders_id"), "orders", ["id"], unique=False)
    op.create_index(op.f("ix_orders_user_id"), "orders", ["user_id"], unique=False)

    op.create_table(
        "products",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("category_id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=150), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("price", sa.Numeric(10, 2), nullable=False),
        sa.Column("image_url", sa.String(length=500), nullable=True),
        sa.Column("calories", sa.Integer(), nullable=True),
        sa.Column("weight", sa.Integer(), nullable=True),
        sa.Column("volume", sa.Integer(), nullable=True),
        sa.Column("is_available", sa.Boolean(), nullable=False),
        sa.Column("is_preorder_available", sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(["category_id"], ["categories.id"], ondelete="RESTRICT"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_products_category_id"), "products", ["category_id"], unique=False)
    op.create_index(op.f("ix_products_id"), "products", ["id"], unique=False)

    op.create_table(
        "profiles",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("first_name", sa.String(length=100), nullable=True),
        sa.Column("last_name", sa.String(length=100), nullable=True),
        sa.Column("phone", sa.String(length=30), nullable=True),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("user_id"),
    )
    op.create_index(op.f("ix_profiles_id"), "profiles", ["id"], unique=False)

    op.create_table(
        "referrals",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("inviter_id", sa.Integer(), nullable=False),
        sa.Column("invited_user_id", sa.Integer(), nullable=False),
        sa.Column("bonus_awarded", sa.Boolean(), nullable=False),
        sa.Column("bonus_awarded_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["invited_user_id"], ["users.id"]),
        sa.ForeignKeyConstraint(["inviter_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_referrals_id"), "referrals", ["id"], unique=False)
    op.create_index(op.f("ix_referrals_invited_user_id"), "referrals", ["invited_user_id"], unique=True)
    op.create_index(op.f("ix_referrals_inviter_id"), "referrals", ["inviter_id"], unique=False)

    op.create_table(
        "bonus_transactions",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("card_id", sa.Integer(), nullable=False),
        sa.Column("order_id", sa.Integer(), nullable=True),
        sa.Column("transaction_type", sa.String(length=30), nullable=False),
        sa.Column("amount", sa.Numeric(10, 2), nullable=False),
        sa.Column("description", sa.String(length=255), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["card_id"], ["loyalty_cards.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["order_id"], ["orders.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_bonus_transactions_card_id"), "bonus_transactions", ["card_id"], unique=False)
    op.create_index(op.f("ix_bonus_transactions_id"), "bonus_transactions", ["id"], unique=False)
    op.create_index(op.f("ix_bonus_transactions_order_id"), "bonus_transactions", ["order_id"], unique=False)

    op.create_table(
        "order_items",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("order_id", sa.Integer(), nullable=False),
        sa.Column("product_id", sa.Integer(), nullable=False),
        sa.Column("product_name", sa.String(length=150), nullable=False),
        sa.Column("quantity", sa.Integer(), nullable=False),
        sa.Column("unit_price", sa.Numeric(10, 2), nullable=False),
        sa.Column("total_price", sa.Numeric(10, 2), nullable=False),
        sa.ForeignKeyConstraint(["order_id"], ["orders.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["product_id"], ["products.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_order_items_id"), "order_items", ["id"], unique=False)
    op.create_index(op.f("ix_order_items_order_id"), "order_items", ["order_id"], unique=False)
    op.create_index(op.f("ix_order_items_product_id"), "order_items", ["product_id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_order_items_product_id"), table_name="order_items")
    op.drop_index(op.f("ix_order_items_order_id"), table_name="order_items")
    op.drop_index(op.f("ix_order_items_id"), table_name="order_items")
    op.drop_table("order_items")

    op.drop_index(op.f("ix_bonus_transactions_order_id"), table_name="bonus_transactions")
    op.drop_index(op.f("ix_bonus_transactions_id"), table_name="bonus_transactions")
    op.drop_index(op.f("ix_bonus_transactions_card_id"), table_name="bonus_transactions")
    op.drop_table("bonus_transactions")

    op.drop_index(op.f("ix_referrals_inviter_id"), table_name="referrals")
    op.drop_index(op.f("ix_referrals_invited_user_id"), table_name="referrals")
    op.drop_index(op.f("ix_referrals_id"), table_name="referrals")
    op.drop_table("referrals")

    op.drop_index(op.f("ix_profiles_id"), table_name="profiles")
    op.drop_table("profiles")

    op.drop_index(op.f("ix_products_id"), table_name="products")
    op.drop_index(op.f("ix_products_category_id"), table_name="products")
    op.drop_table("products")

    op.drop_index(op.f("ix_orders_user_id"), table_name="orders")
    op.drop_index(op.f("ix_orders_id"), table_name="orders")
    op.drop_table("orders")

    op.drop_index(op.f("ix_loyalty_cards_user_id"), table_name="loyalty_cards")
    op.drop_index(op.f("ix_loyalty_cards_id"), table_name="loyalty_cards")
    op.drop_table("loyalty_cards")

    op.drop_index(op.f("ix_users_referral_code"), table_name="users")
    op.drop_index(op.f("ix_users_id"), table_name="users")
    op.drop_index(op.f("ix_users_email"), table_name="users")
    op.drop_table("users")

    op.drop_index(op.f("ix_promotions_id"), table_name="promotions")
    op.drop_table("promotions")

    op.drop_index(op.f("ix_coffee_shops_id"), table_name="coffee_shops")
    op.drop_table("coffee_shops")

    op.drop_index(op.f("ix_categories_name"), table_name="categories")
    op.drop_index(op.f("ix_categories_id"), table_name="categories")
    op.drop_table("categories")
