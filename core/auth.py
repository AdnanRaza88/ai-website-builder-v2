from datetime import datetime, timedelta
from typing import Optional
import bcrypt
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from core.config import settings
from core.models import User


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode(), hashed.encode())


def make_token(data: dict) -> str:
    payload = data.copy()
    payload["exp"] = datetime.utcnow() + timedelta(days=settings.JWT_EXPIRE_DAYS)
    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGO)


def decode_token(token: str) -> Optional[dict]:
    try:
        return jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGO])
    except JWTError:
        return None


def auth_user(db: Session, email: str, password: str) -> Optional[User]:
    u = db.query(User).filter(User.email == email.lower().strip()).first()
    if u and verify_password(password, u.password_hash):
        return u
    return None


def create_user(db: Session, email: str, password: str, display_name: str) -> User:
    u = User(
        email=email.lower().strip(),
        password_hash=hash_password(password),
        display_name=display_name.strip() or email.split("@")[0],
    )
    db.add(u)
    db.commit()
    db.refresh(u)
    return u
