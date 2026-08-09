from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import provider_required
from app.models.user import User
from app.schemas.service import (
    ServiceCreate,
    ServiceUpdate,
    ServiceResponse,
)
from app.repository.service import (
    create_service,
    get_services,
    get_service,
    update_service,
    delete_service,
)

router = APIRouter(
    prefix="/services",
    tags=["Services"],
)


@router.post("", response_model=ServiceResponse)
def add_service(
    service: ServiceCreate,
    db: Session = Depends(get_db),
    provider: User = Depends(provider_required),
):
    return create_service(db, service, provider)


@router.get("", response_model=list[ServiceResponse])
def view_services(
    search: str = None,
    category: str = None,
    min_price: float = None,
    max_price: float = None,
    db: Session = Depends(get_db),
):
    return get_services(
        db,
        search,
        category,
        min_price,
        max_price,
    )


@router.get("/{service_id}", response_model=ServiceResponse)
def view_service(
    service_id: int,
    db: Session = Depends(get_db),
):
    service = get_service(db, service_id)

    if not service:
        raise HTTPException(404, "Service not found")

    return service


@router.put("/{service_id}")
def edit_service(
    service_id: int,
    updated_service: ServiceUpdate,
    db: Session = Depends(get_db),
    provider: User = Depends(provider_required),
):
    service = get_service(db, service_id)

    if not service:
        raise HTTPException(404, "Service not found")

    if service.provider_id != provider.id:
        raise HTTPException(403, "Not authorized")

    return update_service(
        db,
        service,
        updated_service,
    )


@router.delete("/{service_id}")
def remove_service(
    service_id: int,
    db: Session = Depends(get_db),
    provider: User = Depends(provider_required),
):
    service = get_service(db, service_id)

    if not service:
        raise HTTPException(404, "Service not found")

    if service.provider_id != provider.id:
        raise HTTPException(403, "Not authorized")

    delete_service(db, service)

    return {"message": "Service deleted successfully"}