from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.auth.schemas import LoginRequest, Token
from app.auth.service import AuthService
from app.database import get_db
from app.users.repository import UserRepository
from app.users.schemas import UserCreate, UserRead
from app.users.service import UserService


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    repository = UserRepository(db)
    service = UserService(repository)
    return service.register_user(user_data)


@router.post("/login", response_model=Token)
def login(credentials: LoginRequest, db: Session = Depends(get_db)):
    repository = UserRepository(db)
    service = AuthService(repository)
    return service.login(credentials)
