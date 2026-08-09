from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.models.service import Service
from app.models.user import User
from app.schemas.service import ServiceCreate, ServiceUpdate


def create_service(db: Session, service: ServiceCreate, provider: User):
    new_service = Service(
        name=service.name,
        description=service.description,
        category=service.category,
        duration=service.duration,
        price=service.price,
        provider_id=provider.id,
    )

    db.add(new_service)
    db.commit()
    db.refresh(new_service)

    return new_service


def get_services(
    db: Session,
    search: str = None,
    category: str = None,
    min_price: float = None,
    max_price: float = None,
):
    query = db.query(Service)

    if search:
        query = query.filter(
            or_(
                Service.name.ilike(f"%{search}%"),
                Service.description.ilike(f"%{search}%"),
            )
        )

    if category:
        query = query.filter(Service.category == category)

    if min_price is not None:
        query = query.filter(Service.price >= min_price)

    if max_price is not None:
        query = query.filter(Service.price <= max_price)

    return query.all()


def get_service(db: Session, service_id: int):
    return db.query(Service).filter(Service.id == service_id).first()


def update_service(
    db: Session,
    db_service: Service,
    service: ServiceUpdate,
):
    data = service.model_dump(exclude_unset=True)

    for key, value in data.items():
        setattr(db_service, key, value)

    db.commit()
    db.refresh(db_service)

    return db_service


def delete_service(db: Session, db_service: Service):
    db.delete(db_service)
    db.commit()