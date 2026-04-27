from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator


class ProfileRead(BaseModel):
    id: int
    first_name: str | None = None
    last_name: str | None = None
    phone: str | None = None

    model_config = ConfigDict(from_attributes=True)


class UserCreate(BaseModel):
    email: str = Field(..., max_length=255)
    password: str = Field(..., min_length=8, max_length=128)
    first_name: str | None = Field(default=None, max_length=100)
    last_name: str | None = Field(default=None, max_length=100)
    phone: str | None = Field(default=None, max_length=30)

    @field_validator("email")
    @classmethod
    def validate_email(cls, value: str) -> str:
        normalized = value.strip().lower()
        if "@" not in normalized or "." not in normalized.split("@")[-1]:
            raise ValueError("Invalid email address")
        return normalized


class UserRead(BaseModel):
    id: int
    email: str
    is_active: bool
    created_at: datetime
    profile: ProfileRead | None = None

    model_config = ConfigDict(from_attributes=True)
