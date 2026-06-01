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

def user_payload(user: User, business_id: str | None = None, favorites_count: int = 0) -> dict:
    # ... (Sin cambios)


# NUEVA FUNCIÓN
def business_payload(business: Business, services_count: int = 0, active_services_count: int = 0, category_name: str | None = None) -> dict:
    return {
        "id": business.id,
        "owner_user_id": business.owner_user_id,
        "name": business.name,
        "category_id": business.category_id,
        "category_name": category_name,
        "description": business.description,
        "phone": business.phone,
        "email": business.email,
        "address": business.address,
        "city": business.city,
        "featured": business.featured,
        "availability_status": business.availability_status,
        "rating": business.rating,
        "reviews_count": business.reviews_count,
        "image_url": business.image_url,
        "team": business.team or [],
        "gallery": business.gallery or [],
        "weekly_hours": business.weekly_hours or {},
        "services_count": services_count,
        "active_services_count": active_services_count,
        "created_at": business.created_at,
        "updated_at": business.updated_at,
    }

# NUEVA FUNCIÓN
def service_payload(service: Service) -> dict:
    return {
        "id": service.id,
        "business_id": service.business_id,
        "name": service.name,
        "description": service.description,
        "duration_minutes": service.duration_minutes,
        "price": service.price,
        "active": service.active,
        "weekly_hours": service.weekly_hours or {},
        "professionals": service.professionals or [],
        "created_at": service.created_at,
        "updated_at": service.updated_at,
    }