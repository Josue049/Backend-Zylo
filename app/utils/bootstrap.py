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

business_owner = User(
        id=make_id("user"),
        name="Demo Business",
        email="business@zylo.test",
        password_hash=hash_password("Demo1234!"),
        phone="+1 555 0100",
        location="Centro",
        role="business_owner",
    )
    client = User(
        id=make_id("user"),
        name="Demo Client",
        email="client@zylo.test",
        password_hash=hash_password("Demo1234!"),
        phone="+1 555 0110",
        location="Norte",
        role="client",
    )
    db.add_all([business_owner, client])
    db.flush()