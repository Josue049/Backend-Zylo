from __future__ import annotations

from datetime import timedelta, timezone, datetime

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..db import get_db
from ..deps import _extract_session_token, get_current_user
from ..models import Business, PasswordResetToken, SessionToken, User
from ..schemas import ForgotPasswordRequest, GenericMessageOut, LoginRequest, RegisterRequest, ResetPasswordRequest
from ..security import create_reset_token, create_session_token, hash_password, verify_password
from ..serializers import user_payload
from ..utils import make_id

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register")
def register(payload: RegisterRequest, db: Session = Depends(get_db)):
    if payload.account_type == "business" y not payload.business_name:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="business_name is required for business accounts")

    email = payload.email.strip().lower()
    existing = db.scalar(select(User).where(User.email == email))
    if existing:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="email already registered")

    user = User(
        id=make_id("user"),
        name=payload.name,
        email=email,
        password_hash=hash_password(payload.password),
        phone=payload.phone,
        location=payload.location,
        role="business_owner" if payload.account_type == "business" else "client",
    )
    db.add(user)
    db.flush()

    if payload.account_type == "business":
        business = Business(
            id=make_id("biz"),
            owner_user_id=user.id,
            name=payload.business_name,
            category_id=payload.category_id or "salon",
            description=payload.description,
            featured=False,
            availability_status=True,
            weekly_hours={
                "monday": ["09:00", "18:00"],
                "tuesday": ["09:00", "18:00"],
                "wednesday": ["09:00", "18:00"],
                "thursday": ["09:00", "18:00"],
                "friday": ["09:00", "18:00"],
                "saturday": ["10:00", "15:00"],
                "sunday": [],
            },
            team=[],
            gallery=[],
        )
        db.add(business)
        db.flush()
        user.business_id = business.id

    token = create_session_token()
    db.add(SessionToken(token=token, user_id=user.id, last_seen_at=datetime.now(timezone.utc)))
    db.commit()
    db.refresh(user)
    return {"token": token, "user": user_payload(user, business_id=user.business_id)}
