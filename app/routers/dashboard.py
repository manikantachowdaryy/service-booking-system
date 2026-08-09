from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import (
    admin_required,
    provider_required,
    customer_required,
)
from app.models.user import User

from app.schemas.dashboard import (
    AdminDashboardResponse,
    ProviderDashboardResponse,
    CustomerDashboardResponse,
)

from app.repository.dashboard import (
    get_admin_dashboard,
    get_provider_dashboard,
    get_customer_dashboard,
)

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"],
)


@router.get(
    "/admin",
    response_model=AdminDashboardResponse,
)
def admin_dashboard(
    db: Session = Depends(get_db),
    admin: User = Depends(admin_required),
):
    return get_admin_dashboard(db)


@router.get(
    "/provider",
    response_model=ProviderDashboardResponse,
)
def provider_dashboard(
    db: Session = Depends(get_db),
    provider: User = Depends(provider_required),
):
    return get_provider_dashboard(db, provider)


@router.get(
    "/customer",
    response_model=CustomerDashboardResponse,
)
def customer_dashboard(
    db: Session = Depends(get_db),
    customer: User = Depends(customer_required),
):
    return get_customer_dashboard(db, customer)