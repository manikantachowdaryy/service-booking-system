from datetime import date, time
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class BookingStatus(str, Enum):
    PENDING = "Pending"
    CONFIRMED = "Confirmed"
    COMPLETED = "Completed"
    CANCELLED = "Cancelled"


class BookingCreate(BaseModel):
    service_id: int
    appointment_date: date
    appointment_time: time
    notes: Optional[str] = None


class BookingUpdate(BaseModel):
    appointment_date: Optional[date] = None
    appointment_time: Optional[time] = None
    status: Optional[BookingStatus] = None
    notes: Optional[str] = None


class BookingResponse(BaseModel):
    id: int
    customer_id: int
    provider_id: int
    service_id: int
    appointment_date: date
    appointment_time: time
    status: BookingStatus
    notes: Optional[str]

    class Config:
        from_attributes = True