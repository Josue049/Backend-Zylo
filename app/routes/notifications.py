from __future__ import annotations

from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..db import get_db
from ..deps import get_current_business, get_current_user
from ..models import Notification, User
from ..schemas import NotificationCreateRequest
from ..serializers import notification_payload
from ..utils import make_id

router = APIRouter(prefix="/notifications", tags=["notifications"])


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


def user_notification_items(user: User, db: Session) -> list[Notification]:
    return list(
        db.scalars(
            select(Notification)
            .where(Notification.recipient_user_id == user.id)
            .order_by(Notification.created_at.desc())
        )
    )


@router.get("")
def list_notifications(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return {
        "items": [
            notification_payload(notification)
            for notification in user_notification_items(current_user, db)
        ]
    }


@router.post("")
def create_notification_from_business(payload: NotificationCreateRequest, current_business=Depends(get_current_business), db: Session = Depends(get_db)):
    recipient = db.get(User, payload.recipient_user_id)
    if not recipient:
        raise HTTPException(status_code=404, detail="Recipient user not found")
    notification = Notification(
        id=make_id("note"),
        recipient_user_id=payload.recipient_user_id,
        type=payload.type,
        title=payload.title,
        message=payload.message,
        read=False,
    )
    del current_business
    db.add(notification)
    db.commit()
    db.refresh(notification)
    return {"notification": notification_payload(notification)}


