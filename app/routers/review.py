from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import customer_required
from app.models.user import User

from app.schemas.review import (
    ReviewCreate,
    ReviewUpdate,
    ReviewResponse,
)

from app.repository.review import (
    create_review,
    get_all_reviews,
    get_review,
    update_review,
    delete_review,
)

router = APIRouter(
    prefix="/reviews",
    tags=["Reviews"],
)


@router.post("", response_model=ReviewResponse)
def add_review(
    review: ReviewCreate,
    db: Session = Depends(get_db),
    customer: User = Depends(customer_required),
):
    result = create_review(db, review, customer)

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Booking not found",
        )

    if result == "NOT_YOUR_BOOKING":
        raise HTTPException(
            status_code=403,
            detail="You can review only your own booking",
        )

    if result == "BOOKING_NOT_COMPLETED":
        raise HTTPException(
            status_code=400,
            detail="Booking must be completed before reviewing",
        )

    if result == "REVIEW_EXISTS":
        raise HTTPException(
            status_code=400,
            detail="Review already exists for this booking",
        )

    return result


@router.get("", response_model=list[ReviewResponse])
def view_reviews(
    db: Session = Depends(get_db),
):
    return get_all_reviews(db)


@router.get("/{review_id}", response_model=ReviewResponse)
def view_review(
    review_id: int,
    db: Session = Depends(get_db),
):
    review = get_review(db, review_id)

    if review is None:
        raise HTTPException(
            status_code=404,
            detail="Review not found",
        )

    return review


@router.put("/{review_id}", response_model=ReviewResponse)
def edit_review(
    review_id: int,
    review: ReviewUpdate,
    db: Session = Depends(get_db),
):
    db_review = get_review(db, review_id)

    if db_review is None:
        raise HTTPException(
            status_code=404,
            detail="Review not found",
        )

    return update_review(
        db,
        db_review,
        review,
    )


@router.delete("/{review_id}")
def remove_review(
    review_id: int,
    db: Session = Depends(get_db),
):
    db_review = get_review(db, review_id)

    if db_review is None:
        raise HTTPException(
            status_code=404,
            detail="Review not found",
        )

    delete_review(db, db_review)

    return {
        "message": "Review deleted successfully"
    }