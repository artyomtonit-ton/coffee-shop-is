from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.users.models import Profile, User
from app.users.schemas import UserCreate


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, user_id: int) -> User | None:
        statement = (
            select(User)
            .options(selectinload(User.profile))
            .where(User.id == user_id)
        )
        return self.db.scalar(statement)

    def get_by_email(self, email: str) -> User | None:
        statement = (
            select(User)
            .options(selectinload(User.profile))
            .where(User.email == email)
        )
        return self.db.scalar(statement)

    def create(self, user_data: UserCreate, hashed_password: str) -> User:
        user = User(
            email=user_data.email,
            hashed_password=hashed_password,
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
