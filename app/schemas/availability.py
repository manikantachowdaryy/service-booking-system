from datetime import time
from typing import Optional

from pydantic import BaseModel, field_validator


class AvailabilityCreate(BaseModel):
    day_of_week: str
    start_time: time
    end_time: time
    is_available: bool = True

    @field_validator("end_time")
    @classmethod
    def validate_end_time(
        cls,
        end_time: time,
        info,
    ):
        start_time = info.data.get("start_time")

        if start_time is not None and end_time <= start_time:
            raise ValueError(
                "End time must be after start time"
            )

        return end_time


class AvailabilityUpdate(BaseModel):
    day_of_week: Optional[str] = None
    start_time: Optional[time] = None
    end_time: Optional[time] = None
    is_available: Optional[bool] = None


class AvailabilityResponse(BaseModel):
    id: int
    provider_id: int
    day_of_week: str
    start_time: time
    end_time: time
    is_available: bool

    class Config:
        from_attributes = True