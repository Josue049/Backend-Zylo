from __future__ import annotations

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from ..cloudinary_api import upload_image_bytes
from ..db import get_db, settings
from ..deps import get_current_user
from ..models import Booking, Business, Favorite, Service, User
from ..schemas import UpdateUserRequest
from ..serializers import business_payload, booking_payload, user_payload

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/me")
def me(current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    favorites_count = db.scalar(select(func.count()).select_from(Favorite).where(Favorite.user_id == current_user.id)) or 0
    return {"user": user_payload(current_user, business_id=current_user.business_id, favorites_count=favorites_count)}

@router.patch("/me")
def update_me(payload: UpdateUserRequest, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    for field_name in ["name", "phone", "location", "bio"]:
        value = getattr(payload, field_name)
        if value is not None:
            setattr(current_user, field_name, value)
    db.commit()
    favorites_count = db.scalar(select(func.count()).select_from(Favorite).where(Favorite.user_id == current_user.id)) or 0
    return {"user": user_payload(current_user, business_id=current_user.business_id, favorites_count=favorites_count)}