from datetime import datetime

from sqlalchemy.orm import Session

from app.models.booking import Booking
from app.models.service import Service
from app.models.availability import Availability
from app.models.user import User
from app.schemas.booking import (
    BookingCreate,
    BookingUpdate,
    BookingStatus,
)
from app.repository.notification import create_notification_for_user


def create_booking(
    db: Session,
    booking: BookingCreate,
    customer: User,
):
    appointment_datetime = datetime.combine(
        booking.appointment_date,
        booking.appointment_time,
    )

    if appointment_datetime <= datetime.now():
        return "PAST_APPOINTMENT"

    service = (
        db.query(Service)
        .filter(Service.id == booking.service_id)
        .first()
    )

    if service is None:
        return None

    availability = (
        db.query(Availability)
        .filter(
            Availability.provider_id == service.provider_id,
            Availability.day_of_week
            == booking.appointment_date.strftime("%A"),
            Availability.is_available == True,
        )
        .first()
    )

    if availability is None:
        return "NOT_AVAILABLE"

    if (
        booking.appointment_time < availability.start_time
        or booking.appointment_time >= availability.end_time
    ):
        return "OUTSIDE_AVAILABILITY"

    existing_booking = (
        db.query(Booking)
        .filter(
            Booking.provider_id == service.provider_id,
            Booking.appointment_date == booking.appointment_date,
            Booking.appointment_time == booking.appointment_time,
            Booking.status != BookingStatus.CANCELLED.value,
        )
        .first()
    )

    if existing_booking:
        return "SLOT_BOOKED"

    new_booking = Booking(
        customer_id=customer.id,
        provider_id=service.provider_id,
        service_id=service.id,
        appointment_date=booking.appointment_date,
        appointment_time=booking.appointment_time,
        status=BookingStatus.PENDING.value,
        notes=booking.notes,
    )

    db.add(new_booking)
    db.flush()

    # Notify customer
    create_notification_for_user(
        db=db,
        user_id=customer.id,
        title="Booking Created",
        message=(
            f"Your booking #{new_booking.id} has been "
            "created successfully."
        ),
        booking_id=new_booking.id,
    )

    # Notify provider
    create_notification_for_user(
        db=db,
        user_id=service.provider_id,
        title="New Booking",
        message=(
            f"You have received a new booking "
            f"#{new_booking.id}."
        ),
        booking_id=new_booking.id,
    )

    db.commit()
    db.refresh(new_booking)

    return new_booking


def get_all_bookings(db: Session):
    return db.query(Booking).all()


def get_booking(
    db: Session,
    booking_id: int,
):
    return (
        db.query(Booking)
        .filter(Booking.id == booking_id)
        .first()
    )


def update_booking(
    db: Session,
    db_booking: Booking,
    booking: BookingUpdate,
):
    data = booking.model_dump(exclude_unset=True)

    if "status" in data:
        new_status = data["status"]

        if isinstance(new_status, BookingStatus):
            new_status = new_status.value

        current_status = db_booking.status

        allowed_transitions = {
            BookingStatus.PENDING.value: {
                BookingStatus.CONFIRMED.value,
                BookingStatus.CANCELLED.value,
            },
            BookingStatus.CONFIRMED.value: {
                BookingStatus.COMPLETED.value,
                BookingStatus.CANCELLED.value,
            },
            BookingStatus.COMPLETED.value: set(),
            BookingStatus.CANCELLED.value: set(),
        }

        if new_status != current_status:
            allowed = allowed_transitions.get(
                current_status,
                set(),
            )

            if new_status not in allowed:
                return "INVALID_STATUS_TRANSITION"

        data["status"] = new_status

    for key, value in data.items():
        setattr(db_booking, key, value)

    db.commit()
    db.refresh(db_booking)

    return db_booking


def delete_booking(
    db: Session,
    db_booking: Booking,
):
    db.delete(db_booking)
    db.commit()