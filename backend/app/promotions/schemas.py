from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field, model_validator


class PromotionBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=150)
    description: str = Field(..., min_length=1)
    discount_percent: int = Field(..., ge=1, le=100)
    start_date: date
    end_date: date
    is_active: bool = True

    @model_validator(mode="after")
    def validate_dates(self):
        if self.end_date < self.start_date:
            raise ValueError("end_date must be greater than or equal to start_date")
        return self


class PromotionCreate(PromotionBase):
    pass


class PromotionUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=150)
    description: str | None = Field(default=None, min_length=1)
    discount_percent: int | None = Field(default=None, ge=1, le=100)
    start_date: date | None = None
    end_date: date | None = None
    is_active: bool | None = None

    @model_validator(mode="after")
    def validate_dates(self):
        if (
            self.start_date is not None
            and self.end_date is not None
            and self.end_date < self.start_date
        ):
            raise ValueError("end_date must be greater than or equal to start_date")
        return self


class PromotionRead(PromotionBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
