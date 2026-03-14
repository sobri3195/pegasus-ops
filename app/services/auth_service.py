from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.core.security import hash_password, verify_password
from app.models.user import User
from app.schemas.auth import RegisterInput


class EmailAlreadyRegisteredError(ValueError):
    pass


def register_user(db: Session, payload: RegisterInput) -> User:
    normalized_email = payload.email.strip().lower()
    existing = db.scalar(select(User).where(func.lower(User.email) == normalized_email))
    if existing:
        raise EmailAlreadyRegisteredError("Email sudah terdaftar")

    user = User(name=payload.name.strip(), email=normalized_email, password_hash=hash_password(payload.password), role="member")
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def authenticate_user(db: Session, email: str, password: str) -> User | None:
    normalized_email = email.strip().lower()
    user = db.scalar(select(User).where(func.lower(User.email) == normalized_email))
    if not user or not verify_password(password, user.password_hash):
        return None
    return user
