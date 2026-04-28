from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.users.models import Profile, Role, User
from app.users.schemas import UserCreate


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, user_id: int) -> User | None:
        statement = (
            select(User)
            .options(selectinload(User.profile), selectinload(User.role))
            .where(User.id == user_id)
        )
        return self.db.scalar(statement)

    def get_by_email(self, email: str) -> User | None:
        statement = (
            select(User)
            .options(selectinload(User.profile), selectinload(User.role))
            .where(User.email == email)
        )
        return self.db.scalar(statement)

    def get_by_referral_code(self, referral_code: str) -> User | None:
        statement = (
            select(User)
            .options(selectinload(User.profile), selectinload(User.role))
            .where(User.referral_code == referral_code)
        )
        return self.db.scalar(statement)

    def get_role_by_name(self, name: str) -> Role | None:
        statement = select(Role).where(Role.name == name)
        return self.db.scalar(statement)

    def get_or_create_role(self, name: str) -> Role:
        role = self.get_role_by_name(name)
        if role is not None:
            return role

        role = Role(name=name)
        self.db.add(role)
        self.db.commit()
        self.db.refresh(role)
        return role

    def create(
        self,
        user_data: UserCreate,
        hashed_password: str,
        referral_code: str,
    ) -> User:
        role = self.get_or_create_role("user")
        user = User(
            role_id=role.id,
            email=user_data.email,
            hashed_password=hashed_password,
            referral_code=referral_code,
            profile=Profile(
                first_name=user_data.first_name,
                last_name=user_data.last_name,
                phone=user_data.phone,
            ),
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return self.get_by_id(user.id) or user

    def update_referral_code(self, user: User, referral_code: str) -> User:
        user.referral_code = referral_code
        self.db.commit()
        self.db.refresh(user)
        return user
