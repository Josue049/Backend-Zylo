from __future__ import annotations

from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..db import get_db
from ..deps import get_current_business, get_current_user
from ..models import Business, Conversation, Message, User
from ..schemas import ConversationCreateRequest, MessageCreateRequest
from ..serializers import conversation_payload, message_payload
from ..utils import make_id

router = APIRouter(prefix="/conversations", tags=["conversations"])


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


def conversation_visible_to_user(conversation: Conversation, user: User, db: Session) -> bool:
    if user.role == "business_owner":
        business = db.scalar(select(Business).where(Business.owner_user_id == user.id))
        return bool(business and conversation.business_id == business.id)
    return conversation.user_id == user.id
