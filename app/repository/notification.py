from sqlalchemy.orm import Session

from app.models.notification import Notification
from app.schemas.notification import NotificationCreate


def create_notification(
    db: Session,
    notification: NotificationCreate,
):
    new_notification = Notification(
        user_id=notification.user_id,
        booking_id=notification.booking_id,
        title=notification.title,
        message=notification.message,
    )

    db.add(new_notification)
    db.commit()
    db.refresh(new_notification)

    return new_notification


def create_notification_for_user(
    db: Session,
    user_id: int,
    title: str,
    message: str,
    booking_id: int | None = None,
):
    new_notification = Notification(
        user_id=user_id,
        booking_id=booking_id,
        title=title,
        message=message,
    )

    db.add(new_notification)
    db.flush()

    return new_notification


def get_all_notifications(db: Session):
    return db.query(Notification).all()


def get_notification(
    db: Session,
    notification_id: int,
):
    return (
        db.query(Notification)
        .filter(Notification.id == notification_id)
        .first()
    )


def mark_as_read(
    db: Session,
    notification: Notification,
):
    notification.is_read = True

    db.commit()
    db.refresh(notification)

    return notification


def delete_notification(
    db: Session,
    notification: Notification,
):
    db.delete(notification)
    db.commit()