import secrets
import string

from fastapi import HTTPException, status

from app.common.security import get_password_hash
from app.loyalty.repository import LoyaltyRepository
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
        referral_code = self._generate_unique_referral_code()
        user = self.repository.create(user_data, hashed_password, referral_code)
        LoyaltyRepository(self.repository.db).get_or_create_card(user.id)
        return user

    def get_current_user_profile(self, user: User) -> User:
        return user

    def ensure_referral_code(self, user: User) -> str:
        if user.referral_code:
            return user.referral_code

        if self.repository is None:
            raise RuntimeError("User repository is required")

        referral_code = self._generate_unique_referral_code()
        self.repository.update_referral_code(user, referral_code)
        return referral_code

    def _generate_unique_referral_code(self) -> str:
        if self.repository is None:
            raise RuntimeError("User repository is required")

        alphabet = string.ascii_uppercase + string.digits
        while True:
            referral_code = "".join(secrets.choice(alphabet) for _ in range(8))
            if self.repository.get_by_referral_code(referral_code) is None:
                return referral_code
