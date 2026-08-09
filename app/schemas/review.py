from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class ReviewCreate(BaseModel):
    booking_id: int
    rating: int = Field(..., ge=1, le=5)
    review: Optional[str] = Field(
        default=None,
        max_length=1000,
    )


class ReviewUpdate(BaseModel):
    rating: int = Field(..., ge=1, le=5)
    review: Optional[str] = Field(
        default=None,
        max_length=1000,
    )


class ReviewResponse(BaseModel):
    id: int
    booking_id: int
    customer_id: int
    service_id: int
    rating: int
    review: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True