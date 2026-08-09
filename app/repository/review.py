from sqlalchemy.orm import Session

from app.models.review import Review
from app.models.booking import Booking
from app.schemas.review import (
    ReviewCreate,
    ReviewUpdate,
)
from app.models.user import User


def create_review(
    db: Session,
    review: ReviewCreate,
    customer: User,
):
    booking = (
        db.query(Booking)
        .filter(Booking.id == review.booking_id)
        .first()
    )

    if booking is None:
        return None

    if booking.customer_id != customer.id:
        return "NOT_YOUR_BOOKING"

    if booking.status != "Completed":
        return "BOOKING_NOT_COMPLETED"

    existing_review = (
        db.query(Review)
        .filter(Review.booking_id == review.booking_id)
        .first()
    )

    if existing_review:
        return "REVIEW_EXISTS"

    new_review = Review(
        booking_id=booking.id,
        customer_id=customer.id,
        service_id=booking.service_id,
        rating=review.rating,
        review=review.review,
    )

    db.add(new_review)
    db.commit()
    db.refresh(new_review)

    return new_review


def get_all_reviews(db: Session):
    return db.query(Review).all()


def get_review(db: Session, review_id: int):
    return (
        db.query(Review)
        .filter(Review.id == review_id)
        .first()
    )


def update_review(
    db: Session,
    db_review: Review,
    review: ReviewUpdate,
):
    db_review.rating = review.rating
    db_review.review = review.review

    db.commit()
    db.refresh(db_review)

    return db_review


def delete_review(
    db: Session,
    db_review: Review,
):
    db.delete(db_review)
    db.commit()