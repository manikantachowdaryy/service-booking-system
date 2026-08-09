from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.notification import (
    NotificationCreate,
    NotificationResponse,
)
from app.repository.notification import (
    create_notification,
    get_all_notifications,
    get_notification,
    mark_as_read,
    delete_notification,
)

router = APIRouter(
    prefix="/notifications",
    tags=["Notifications"],
)


@router.post("", response_model=NotificationResponse)
def add_notification(
    notification: NotificationCreate,
    db: Session = Depends(get_db),
):
    return create_notification(db, notification)


@router.get("", response_model=list[NotificationResponse])
def view_notifications(
    db: Session = Depends(get_db),
):
    return get_all_notifications(db)


@router.get(
    "/{notification_id}",
    response_model=NotificationResponse,
)
def view_notification(
    notification_id: int,
    db: Session = Depends(get_db),
):
    notification = get_notification(db, notification_id)

    if notification is None:
        raise HTTPException(
            status_code=404,
            detail="Notification not found",
        )

    return notification


@router.put(
    "/{notification_id}/read",
    response_model=NotificationResponse,
)
def read_notification(
    notification_id: int,
    db: Session = Depends(get_db),
):
    notification = get_notification(db, notification_id)

    if notification is None:
        raise HTTPException(
            status_code=404,
            detail="Notification not found",
        )

    return mark_as_read(db, notification)


@router.delete("/{notification_id}")
def remove_notification(
    notification_id: int,
    db: Session = Depends(get_db),
):
    notification = get_notification(db, notification_id)

    if notification is None:
        raise HTTPException(
            status_code=404,
            detail="Notification not found",
        )

    delete_notification(db, notification)

    return {
        "message": "Notification deleted successfully"
    }