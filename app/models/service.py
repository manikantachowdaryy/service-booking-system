from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base


class Service(Base):
    __tablename__ = "services"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, nullable=False)
    description = Column(String)
    category = Column(String, nullable=False)
    duration = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)

    status = Column(Boolean, default=True)

    provider_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    provider = relationship(
        "User",
        back_populates="services"
    )

    bookings = relationship(
        "Booking",
        back_populates="service",
        cascade="all, delete-orphan"
    )

    reviews = relationship(
        "Review",
        back_populates="service",
        cascade="all, delete-orphan"
    )