import uuid

from sqlalchemy.orm import Session

from app.models.booking import Booking
from app.models.payment import Payment
from app.schemas.payment import (
    PaymentCreate,
    PaymentUpdate,
    PaymentStatus,
)
from app.repository.notification import create_notification_for_user


def create_payment(
    db: Session,
    payment: PaymentCreate,
):
    booking = (
        db.query(Booking)
        .filter(Booking.id == payment.booking_id)
        .first()
    )

    if booking is None:
        return None

    existing_payment = (
        db.query(Payment)
        .filter(Payment.booking_id == payment.booking_id)
        .first()
    )

    if existing_payment:
        return "PAYMENT_EXISTS"

    new_payment = Payment(
        booking_id=payment.booking_id,
        amount=payment.amount,
        payment_method=payment.payment_method.value,
        payment_status=PaymentStatus.SUCCESS.value,
        transaction_id=str(uuid.uuid4()),
    )

    booking.status = "Confirmed"

    db.add(new_payment)
    db.flush()

    create_notification_for_user(
        db=db,
        user_id=booking.customer_id,
        title="Payment Successful",
        message=(
            f"Payment of ₹{payment.amount} for "
            f"booking #{booking.id} was successful."
        ),
        booking_id=booking.id,
    )

    create_notification_for_user(
        db=db,
        user_id=booking.provider_id,
        title="Booking Confirmed",
        message=(
            f"Booking #{booking.id} has been confirmed "
            "after successful payment."
        ),
        booking_id=booking.id,
    )

    db.commit()
    db.refresh(new_payment)

    return new_payment


def get_all_payments(db: Session):
    return db.query(Payment).all()


def get_payment(
    db: Session,
    payment_id: int,
):
    return (
        db.query(Payment)
        .filter(Payment.id == payment_id)
        .first()
    )


def update_payment(
    db: Session,
    db_payment: Payment,
    payment: PaymentUpdate,
):
    db_payment.payment_status = payment.payment_status.value

    db.commit()
    db.refresh(db_payment)

    return db_payment


def delete_payment(
    db: Session,
    db_payment: Payment,
):
    db.delete(db_payment)
    db.commit()