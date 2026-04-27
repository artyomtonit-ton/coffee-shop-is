from fastapi import HTTPException, status

from app.common.security import get_password_hash
from app.users.models import User
from app.users.repository import UserRepository
from app.users.schemas import UserCreate


class UserService:
    def __init__(self, repository: UserRepository | None = None):
        self.repository = repository

    def register_user(self, user_data: UserCreate) -> User:
        if self.repository is None:
            raise RuntimeError("User repository is required")

        existing_user = self.repository.get_by_email(user_data.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with this email already exists",
            )

        hashed_password = get_password_hash(user_data.password)
        return self.repository.create(user_data, hashed_password)

    def get_current_user_profile(self, user: User) -> User:
        return user
