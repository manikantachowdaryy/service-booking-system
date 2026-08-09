from sqlalchemy import (
    Column,
    Integer,
    Float,
    String,
    DateTime,
    ForeignKey,
)
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.database import Base


class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)

    booking_id = Column(
        Integer,
        ForeignKey("bookings.id"),
        unique=True,
        nullable=False,
    )

    amount = Column(
        Float,
        nullable=False,
    )

    payment_method = Column(
        String,
        nullable=False,
    )

    payment_status = Column(
        String,
        default="Pending",
    )

    transaction_id = Column(
        String,
        unique=True,
        nullable=False,
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    booking = relationship(
        "Booking",
        back_populates="payment",
    )