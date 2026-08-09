from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db

from app.schemas.payment import (
    PaymentCreate,
    PaymentUpdate,
    PaymentResponse,
)

from app.repository.payment import (
    create_payment,
    get_all_payments,
    get_payment,
    update_payment,
    delete_payment,
)

router = APIRouter(
    prefix="/payments",
    tags=["Payments"],
)


@router.post("", response_model=PaymentResponse)
def add_payment(
    payment: PaymentCreate,
    db: Session = Depends(get_db),
):
    result = create_payment(db, payment)

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Booking not found"
        )

    if result == "PAYMENT_EXISTS":
        raise HTTPException(
            status_code=400,
            detail="Payment already exists for this booking"
        )

    return result


@router.get("", response_model=list[PaymentResponse])
def view_payments(
    db: Session = Depends(get_db),
):
    return get_all_payments(db)


@router.get("/{payment_id}", response_model=PaymentResponse)
def view_payment(
    payment_id: int,
    db: Session = Depends(get_db),
):
    payment = get_payment(db, payment_id)

    if payment is None:
        raise HTTPException(
            status_code=404,
            detail="Payment not found"
        )

    return payment


@router.put("/{payment_id}", response_model=PaymentResponse)
def edit_payment(
    payment_id: int,
    payment: PaymentUpdate,
    db: Session = Depends(get_db),
):
    db_payment = get_payment(db, payment_id)

    if db_payment is None:
        raise HTTPException(
            status_code=404,
            detail="Payment not found"
        )

    return update_payment(
        db,
        db_payment,
        payment,
    )


@router.delete("/{payment_id}")
def remove_payment(
    payment_id: int,
    db: Session = Depends(get_db),
):
    db_payment = get_payment(db, payment_id)

    if db_payment is None:
        raise HTTPException(
            status_code=404,
            detail="Payment not found"
        )

    delete_payment(db, db_payment)

    return {
        "message": "Payment deleted successfully"
    }