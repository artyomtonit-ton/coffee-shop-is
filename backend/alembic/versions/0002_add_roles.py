"""add roles

Revision ID: 0002_add_roles
Revises: 0001_initial_schema
Create Date: 2026-04-28 02:30:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "0002_add_roles"
down_revision: Union[str, None] = "0001_initial_schema"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "roles",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=50), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_roles_id"), "roles", ["id"], unique=False)
    op.create_index(op.f("ix_roles_name"), "roles", ["name"], unique=True)

    roles_table = sa.table(
        "roles",
        sa.column("name", sa.String),
    )
    op.bulk_insert(
        roles_table,
        [
            {"name": "user"},
            {"name": "admin"},
        ],
    )

    op.add_column("users", sa.Column("role_id", sa.Integer(), nullable=True))
    op.create_index(op.f("ix_users_role_id"), "users", ["role_id"], unique=False)
    op.create_foreign_key(
        "fk_users_role_id_roles",
        "users",
        "roles",
        ["role_id"],
        ["id"],
    )
    op.execute(
        "UPDATE users SET role_id = (SELECT id FROM roles WHERE name = 'user') "
        "WHERE role_id IS NULL"
    )
    op.alter_column("users", "role_id", existing_type=sa.Integer(), nullable=False)


def downgrade() -> None:
    op.drop_constraint("fk_users_role_id_roles", "users", type_="foreignkey")
    op.drop_index(op.f("ix_users_role_id"), table_name="users")
    op.drop_column("users", "role_id")

    op.drop_index(op.f("ix_roles_name"), table_name="roles")
    op.drop_index(op.f("ix_roles_id"), table_name="roles")
    op.drop_table("roles")
