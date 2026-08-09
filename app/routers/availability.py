from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import provider_required
from app.models.user import User
from app.schemas.availability import (
    AvailabilityCreate,
    AvailabilityUpdate,
    AvailabilityResponse,
)
from app.repository.availability import (
    create_availability,
    get_all_availability,
    get_availability,
    update_availability,
    delete_availability,
)

router = APIRouter(
    prefix="/availability",
    tags=["Availability"],
)


@router.post("", response_model=AvailabilityResponse)
def add_availability(
    availability: AvailabilityCreate,
    db: Session = Depends(get_db),
    provider: User = Depends(provider_required),
):
    return create_availability(db, availability, provider)


@router.get("", response_model=list[AvailabilityResponse])
def view_availability(
    db: Session = Depends(get_db),
):
    return get_all_availability(db)


@router.put("/{availability_id}")
def edit_availability(
    availability_id: int,
    availability: AvailabilityUpdate,
    db: Session = Depends(get_db),
    provider: User = Depends(provider_required),
):
    db_availability = get_availability(db, availability_id)

    if not db_availability:
        raise HTTPException(404, "Availability not found")

    if db_availability.provider_id != provider.id:
        raise HTTPException(403, "Not authorized")

    return update_availability(
        db,
        db_availability,
        availability,
    )


@router.delete("/{availability_id}")
def remove_availability(
    availability_id: int,
    db: Session = Depends(get_db),
    provider: User = Depends(provider_required),
):
    db_availability = get_availability(db, availability_id)

    if not db_availability:
        raise HTTPException(404, "Availability not found")

    if db_availability.provider_id != provider.id:
        raise HTTPException(403, "Not authorized")

    delete_availability(db, db_availability)

    return {
        "message": "Availability deleted successfully"
    }