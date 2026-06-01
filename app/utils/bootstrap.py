from __future__ import annotations

from datetime import datetime, timedelta, timezone

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from .models import Booking, Business, Favorite, Notification, PasswordResetToken, Service, SessionToken, User
from .security import hash_password
from .utils import make_id


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


def seed_demo_data(db: Session) -> None:
    if db.scalar(select(func.count()).select_from(User)):
        return
