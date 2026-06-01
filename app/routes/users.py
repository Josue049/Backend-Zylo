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

@router.post("/me/photo")
async def upload_photo(photo: UploadFile = File(...), current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    if not photo.content_type or not photo.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Only image files are allowed")

    contents = await photo.read()
    if not contents:
        raise HTTPException(status_code=400, detail="Empty file")

    if not settings.cloudinary_cloud_name or not settings.cloudinary_api_key or not settings.cloudinary_api_secret:
        raise HTTPException(status_code=500, detail="Cloudinary is not configured")

    try:
        result = upload_image_bytes(
            cloud_name=settings.cloudinary_cloud_name,
            api_key=settings.cloudinary_api_key,
            api_secret=settings.cloudinary_api_secret,
            folder=settings.cloudinary_upload_folder,
            file_name=photo.filename or "photo",
            file_bytes=contents,
            content_type=photo.content_type,
            public_id=current_user.id,
            timeout_seconds=settings.cloudinary_timeout_seconds,
        )
    except RuntimeError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc

    current_user.photo_url = result["secure_url"]
    db.commit()
    favorites_count = db.scalar(select(func.count()).select_from(Favorite).where(Favorite.user_id == current_user.id)) or 0
    return {"user": user_payload(current_user, business_id=current_user.business_id, favorites_count=favorites_count), "photo_url": current_user.photo_url}