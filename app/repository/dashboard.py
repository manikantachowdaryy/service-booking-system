from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.user import User
from app.models.service import Service
from app.models.booking import Booking
from app.models.payment import Payment
from app.models.review import Review


def get_admin_dashboard(db: Session):

    total_users = db.query(User).count()

    total_providers = (
        db.query(User)
        .filter(User.role == "provider")
        .count()
    )

    total_customers = (
        db.query(User)
        .filter(User.role == "customer")
        .count()
    )

    total_services = db.query(Service).count()

    total_bookings = db.query(Booking).count()

    completed_bookings = (
        db.query(Booking)
        .filter(Booking.status == "Completed")
        .count()
    )

    cancelled_bookings = (
        db.query(Booking)
        .filter(Booking.status == "Cancelled")
        .count()
    )

    total_revenue = (
        db.query(func.coalesce(func.sum(Payment.amount), 0))
        .filter(Payment.payment_status == "Success")
        .scalar()
    )

    return {
        "total_users": total_users,
        "total_providers": total_providers,
        "total_customers": total_customers,
        "total_services": total_services,
        "total_bookings": total_bookings,
        "completed_bookings": completed_bookings,
        "cancelled_bookings": cancelled_bookings,
        "total_revenue": float(total_revenue or 0),
    }


def get_provider_dashboard(
    db: Session,
    provider: User,
):

    total_services = (
        db.query(Service)
        .filter(Service.provider_id == provider.id)
        .count()
    )

    total_bookings = (
        db.query(Booking)
        .filter(Booking.provider_id == provider.id)
        .count()
    )

    pending_bookings = (
        db.query(Booking)
        .filter(
            Booking.provider_id == provider.id,
            Booking.status == "Pending",
        )
        .count()
    )

    completed_bookings = (
        db.query(Booking)
        .filter(
            Booking.provider_id == provider.id,
            Booking.status == "Completed",
        )
        .count()
    )

    cancelled_bookings = (
        db.query(Booking)
        .filter(
            Booking.provider_id == provider.id,
            Booking.status == "Cancelled",
        )
        .count()
    )

    total_revenue = (
        db.query(func.coalesce(func.sum(Payment.amount), 0))
        .join(
            Booking,
            Payment.booking_id == Booking.id,
        )
        .filter(
            Booking.provider_id == provider.id,
            Payment.payment_status == "Success",
        )
        .scalar()
    )

    average_rating = (
        db.query(func.coalesce(func.avg(Review.rating), 0))
        .join(
            Service,
            Review.service_id == Service.id,
        )
        .filter(Service.provider_id == provider.id)
        .scalar()
    )

    return {
        "total_services": total_services,
        "total_bookings": total_bookings,
        "pending_bookings": pending_bookings,
        "completed_bookings": completed_bookings,
        "cancelled_bookings": cancelled_bookings,
        "total_revenue": float(total_revenue or 0),
        "average_rating": round(float(average_rating or 0), 2),
    }


def get_customer_dashboard(
    db: Session,
    customer: User,
):

    upcoming_bookings = (
        db.query(Booking)
        .filter(
            Booking.customer_id == customer.id,
            Booking.status.in_(["Pending", "Confirmed"]),
        )
        .count()
    )

    completed_bookings = (
        db.query(Booking)
        .filter(
            Booking.customer_id == customer.id,
            Booking.status == "Completed",
        )
        .count()
    )

    cancelled_bookings = (
        db.query(Booking)
        .filter(
            Booking.customer_id == customer.id,
            Booking.status == "Cancelled",
        )
        .count()
    )

    total_spent = (
        db.query(func.coalesce(func.sum(Payment.amount), 0))
        .join(
            Booking,
            Payment.booking_id == Booking.id,
        )
        .filter(
            Booking.customer_id == customer.id,
            Payment.payment_status == "Success",
        )
        .scalar()
    )

    return {
        "upcoming_bookings": upcoming_bookings,
        "completed_bookings": completed_bookings,
        "cancelled_bookings": cancelled_bookings,
        "total_spent": float(total_spent or 0),
    }