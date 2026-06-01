from __future__ import annotations

from collections.abc import Iterable

from sqlalchemy import select
from sqlalchemy.orm import Session

from .models import Booking, Business, Conversation, Favorite, Message, Notification, Service, User


def user_payload(user: User, business_id: str | None = None, favorites_count: int = 0) -> dict:
    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "phone": user.phone,
        "location": user.location,
        "photo_url": user.photo_url,
        "bio": user.bio,
        "role": user.role,
        "business_id": business_id if business_id is not None else user.business_id,
        "favorites_count": favorites_count,
        "created_at": user.created_at,
        "updated_at": user.updated_at,
    }