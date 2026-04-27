from fastapi import APIRouter, Depends

from app.common.dependencies import get_current_user
from app.users.models import User
from app.users.schemas import UserRead
from app.users.service import UserService


router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=UserRead)
def get_me(current_user: User = Depends(get_current_user)):
    service = UserService()
    return service.get_current_user_profile(current_user)
