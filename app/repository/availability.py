from sqlalchemy.orm import Session

from app.models.availability import Availability
from app.models.user import User
from app.schemas.availability import (
    AvailabilityCreate,
    AvailabilityUpdate,
)


def create_availability(
    db: Session,
    availability: AvailabilityCreate,
    provider: User,
):
    new_availability = Availability(
        provider_id=provider.id,
        day_of_week=availability.day_of_week,
        start_time=availability.start_time,
        end_time=availability.end_time,
    )

    db.add(new_availability)
    db.commit()
    db.refresh(new_availability)

    return new_availability


def get_all_availability(db: Session):
    return db.query(Availability).all()


def get_availability(db: Session, availability_id: int):
    return (
        db.query(Availability)
        .filter(Availability.id == availability_id)
        .first()
    )


def update_availability(
    db: Session,
    db_availability: Availability,
    availability: AvailabilityUpdate,
):
    data = availability.model_dump()

    for key, value in data.items():
        setattr(db_availability, key, value)

    db.commit()
    db.refresh(db_availability)

    return db_availability


def delete_availability(
    db: Session,
    db_availability: Availability,
):
    db.delete(db_availability)
    db.commit()