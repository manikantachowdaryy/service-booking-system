from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserRegister
from app.auth import hash_password


def register_user(db: Session, user: UserRegister):

    existing_user = db.query(User).filter(User.email == user.email).first()

    if existing_user:
        return None

    new_user = User(
        full_name=user.full_name,
        email=user.email,
        password_hash=hash_password(user.password),
        phone_number=user.phone_number,
        role=user.role.lower(),
        is_active=True,
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user