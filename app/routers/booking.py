from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user, customer_required
from app.models.user import User

from app.schemas.booking import (
    BookingCreate,
    BookingUpdate,
    BookingResponse,
)

from app.repository.booking import (
    create_booking,
    get_all_bookings,
    get_booking,
    update_booking,
    delete_booking,
)

router = APIRouter(
    prefix="/bookings",
    tags=["Bookings"],
)


@router.post("", response_model=BookingResponse)
def add_booking(
    booking: BookingCreate,
    db: Session = Depends(get_db),
    customer: User = Depends(customer_required),
):
    result = create_booking(db, booking, customer)

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Service not found",
        )

    if result == "PAST_APPOINTMENT":
        raise HTTPException(
            status_code=400,
            detail="Appointment date and time must be in the future",
        )

    if result == "NOT_AVAILABLE":
        raise HTTPException(
            status_code=400,
            detail="Provider is not available on this day",
        )

    if result == "OUTSIDE_AVAILABILITY":
        raise HTTPException(
            status_code=400,
            detail="Selected time is outside provider availability",
        )

    if result == "SLOT_BOOKED":
        raise HTTPException(
            status_code=400,
            detail="Selected time slot is already booked",
        )

    return result


@router.get(
    "",
    response_model=list[BookingResponse],
)
def view_bookings(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role == "admin":
        return get_all_bookings(db)

    if current_user.role == "provider":
        return [
            booking
            for booking in get_all_bookings(db)
            if booking.provider_id == current_user.id
        ]

    return [
        booking
        for booking in get_all_bookings(db)
        if booking.customer_id == current_user.id
    ]


@router.get(
    "/{booking_id}",
    response_model=BookingResponse,
)
def view_booking(
    booking_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    booking = get_booking(db, booking_id)

    if booking is None:
        raise HTTPException(
            status_code=404,
            detail="Booking not found",
        )

    if current_user.role == "admin":
        return booking

    if current_user.role == "provider":
        if booking.provider_id != current_user.id:
            raise HTTPException(
                status_code=403,
                detail="You can only access your own provider bookings",
            )

    elif current_user.role == "customer":
        if booking.customer_id != current_user.id:
            raise HTTPException(
                status_code=403,
                detail="You can only access your own bookings",
            )

    return booking


@router.put(
    "/{booking_id}",
    response_model=BookingResponse,
)
def edit_booking(
    booking_id: int,
    booking: BookingUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    db_booking = get_booking(db, booking_id)

    if db_booking is None:
        raise HTTPException(
            status_code=404,
            detail="Booking not found",
        )

    if current_user.role == "admin":
        pass

    elif current_user.role == "provider":
        if db_booking.provider_id != current_user.id:
            raise HTTPException(
                status_code=403,
                detail="You can only manage your own provider bookings",
            )

        if booking.appointment_date is not None:
            raise HTTPException(
                status_code=403,
                detail="Provider cannot change appointment date",
            )

        if booking.appointment_time is not None:
            raise HTTPException(
                status_code=403,
                detail="Provider cannot change appointment time",
            )

        if booking.notes is not None:
            raise HTTPException(
                status_code=403,
                detail="Provider cannot change booking notes",
            )

    elif current_user.role == "customer":
        if db_booking.customer_id != current_user.id:
            raise HTTPException(
                status_code=403,
                detail="You can only manage your own bookings",
            )

        if (
            booking.status is not None
            and booking.status.value != "Cancelled"
        ):
            raise HTTPException(
                status_code=403,
                detail="Customer can only cancel a booking",
            )

    else:
        raise HTTPException(
            status_code=403,
            detail="Invalid user role",
        )

    result = update_booking(
        db,
        db_booking,
        booking,
    )

    if result == "INVALID_STATUS_TRANSITION":
        raise HTTPException(
            status_code=400,
            detail=f"Invalid status transition from '{db_booking.status}'",
        )

    return result


@router.delete("/{booking_id}")
def remove_booking(
    booking_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    db_booking = get_booking(db, booking_id)

    if db_booking is None:
        raise HTTPException(
            status_code=404,
            detail="Booking not found",
        )

    if current_user.role == "admin":
        pass

    elif current_user.role == "customer":
        if db_booking.customer_id != current_user.id:
            raise HTTPException(
                status_code=403,
                detail="You can only delete your own bookings",
            )

    elif current_user.role == "provider":
        if db_booking.provider_id != current_user.id:
            raise HTTPException(
                status_code=403,
                detail="You can only manage your own provider bookings",
            )

    else:
        raise HTTPException(
            status_code=403,
            detail="Invalid user role",
        )

    delete_booking(db, db_booking)

    return {
        "message": "Booking deleted successfully",
    }