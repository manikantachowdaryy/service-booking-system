from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    Time,
    ForeignKey,
)

from sqlalchemy.orm import relationship

from app.database import Base


class Availability(Base):
    __tablename__ = "availability"

    id = Column(Integer, primary_key=True, index=True)

    provider_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    day_of_week = Column(
        String,
        nullable=False
    )

    start_time = Column(
        Time,
        nullable=False
    )

    end_time = Column(
        Time,
        nullable=False
    )

    is_available = Column(
        Boolean,
        default=True
    )

    provider = relationship(
        "User",
        back_populates="availability"
    )