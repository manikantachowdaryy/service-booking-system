from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    full_name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    password_hash = Column(String, nullable=False)
    phone_number = Column(String, nullable=False)
    role = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )

    services = relationship(
        "Service",
        back_populates="provider",
        cascade="all, delete-orphan"
    )

    availability = relationship(
        "Availability",
        back_populates="provider",
        cascade="all, delete-orphan"
    )

    customer_bookings = relationship(
        "Booking",
        foreign_keys="Booking.customer_id",
        back_populates="customer"
    )

    provider_bookings = relationship(
        "Booking",
        foreign_keys="Booking.provider_id",
        back_populates="provider"
    )

    reviews = relationship(
        "Review",
        back_populates="customer",
        cascade="all, delete-orphan"
    )

    notifications = relationship(
        "Notification",
        back_populates="user",
        cascade="all, delete-orphan"
    )