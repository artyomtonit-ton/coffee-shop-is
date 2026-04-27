from datetime import datetime

from pydantic import BaseModel, Field, field_validator


class ReferralCodeRead(BaseModel):
    referral_code: str


class ReferralCodeApply(BaseModel):
    referral_code: str = Field(..., min_length=1, max_length=20)

    @field_validator("referral_code")
    @classmethod
    def normalize_referral_code(cls, value: str) -> str:
        return value.strip().upper()


class InvitedUserRead(BaseModel):
    referral_id: int
    invited_user_id: int
    invited_user_email: str
    bonus_awarded: bool
    created_at: datetime
