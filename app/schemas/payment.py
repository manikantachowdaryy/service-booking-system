from enum import Enum
from datetime import datetime

from pydantic import BaseModel


class PaymentStatus(str, Enum):
    PENDING = "Pending"
    SUCCESS = "Success"
    FAILED = "Failed"
    REFUNDED = "Refunded"


class PaymentMethod(str, Enum):
    UPI = "UPI"
    CARD = "Card"
    NET_BANKING = "Net Banking"
    CASH = "Cash"
    WALLET = "Wallet"


class PaymentCreate(BaseModel):
    booking_id: int
    amount: float
    payment_method: PaymentMethod


class PaymentUpdate(BaseModel):
    payment_status: PaymentStatus


class PaymentResponse(BaseModel):
    id: int
    booking_id: int
    amount: float
    payment_method: PaymentMethod
    payment_status: PaymentStatus
    transaction_id: str
    created_at: datetime

    class Config:
        from_attributes = True