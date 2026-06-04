from __future__ import annotations

from collections import defaultdict
from datetime import datetime, timedelta, timezone, time

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from ..db import get_db
from ..deps import get_current_business, get_current_user
from ..models import AvailabilityBlock, Booking, Business, Review, Service, User
from ..schemas import AvailabilityBlockCreateRequest, BusinessReviewRequest, ServiceCreateRequest, TeamUpdateRequest
from ..serializers import business_payload, service_payload
from ..utils import make_id

router = APIRouter(prefix="/businesses", tags=["businesses"])

CATEGORIES = [
    {"id": "salon", "name": "Salón"},
    {"id": "spa", "name": "Spa"},
    {"id": "barber", "name": "Barbería"},
    {"id": "fitness", "name": "Fitness"},
]


def utcnow() -> datetime:
    return datetime.now(timezone.utc)

def category_name(category_id: str | None) -> str | None:
    if not category_id:
        return None
    match = next((item for item in CATEGORIES if item["id"] == category_id), None)
    return match["name"] if match else category_id


def business_counts(db: Session, business_id: str) -> tuple[int, int]:
    services_count = db.scalar(select(func.count()).select_from(Service).where(Service.business_id == business_id)) or 0
    active_services_count = db.scalar(select(func.count()).select_from(Service).where(Service.business_id == business_id, Service.active.is_(True))) or 0
    return services_count, active_services_count


def serialize_business(db: Session, business: Business) -> dict:
    services_count, active_services_count = business_counts(db, business.id)
    return business_payload(
        business,
        services_count=services_count,
        active_services_count=active_services_count,
        category_name=category_name(business.category_id),
    )


def overlaps(start_a: datetime, end_a: datetime, start_b: datetime, end_b: datetime) -> bool:
    return start_a < end_b and end_a > start_b


def business_is_available(db: Session, business_id: str, start_at: datetime, end_at: datetime, ignore_booking_id: str | None = None) -> bool:
    blocks = db.scalars(select(AvailabilityBlock).where(AvailabilityBlock.business_id == business_id)).all()
    for block in blocks:
        if overlaps(start_at, end_at, block.start_at, block.end_at):
            return False

    bookings = db.scalars(select(Booking).where(Booking.business_id == business_id)).all()
    for booking in bookings:
        if ignore_booking_id and booking.id == ignore_booking_id:
            continue
        if booking.status in {"canceled", "rejected"}:
            continue
        if overlaps(start_at, end_at, booking.start_at, booking.end_at):
            return False
    return True


def business_owned_by_current_user(current_business: Business) -> Business:
    return current_business


def business_team_member_ids(business: Business) -> set[str]:
    return {member.get("id") for member in (business.team or []) if isinstance(member, dict) and member.get("id")}


WEEKDAY_KEYS = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]


def weekday_key(value: datetime) -> str:
    return WEEKDAY_KEYS[value.weekday()]


def parse_clock(value: str) -> time:
    return datetime.strptime(value, "%H:%M").time()


def schedule_allows_slot(schedule: dict | None, start_at: datetime, end_at: datetime) -> bool:
    if not schedule:
        return True
    if start_at.date() != end_at.date():
        return False
    windows = schedule.get(weekday_key(start_at), []) or []
    if len(windows) < 2 or len(windows) % 2 != 0:
        return False
    start_time = start_at.time()
    end_time = end_at.time()
    for index in range(0, len(windows), 2):
        window_start = parse_clock(windows[index])
        window_end = parse_clock(windows[index + 1])
        if window_start <= start_time and end_time <= window_end:
            return True
    return False


def service_allows_slot(service: Service, business: Business, start_at: datetime, end_at: datetime) -> bool:
    schedule = service.weekly_hours or business.weekly_hours or {}
    return schedule_allows_slot(schedule, start_at, end_at)


def recalculate_business_rating(db: Session, business: Business) -> None:
    reviews = list(db.scalars(select(Review).where(Review.business_id == business.id)))
    business.reviews_count = len(reviews)
    business.rating = round(sum(review.rating for review in reviews) / len(reviews), 2) if reviews else 0.0

@router.get("")
def list_businesses(
    search: str | None = Query(default=None),
    category: str | None = Query(default=None),
    featured: bool | None = Query(default=None),
    available: bool | None = Query(default=None),
    db: Session = Depends(get_db),
):
    businesses = list(db.scalars(select(Business).order_by(Business.created_at.desc())))
    if search:
        term = search.lower()
        businesses = [business for business in businesses if term in business.name.lower() or term in (business.description or "").lower()]
    if category:
        businesses = [business for business in businesses if business.category_id == category]
    if featured is not None:
        businesses = [business for business in businesses if business.featured == featured]
    if available is not None:
        businesses = [business for business in businesses if business.availability_status == available]
    return {"items": [serialize_business(db, business) for business in businesses]}

@router.get("/categories")
def list_categories():
    return {"items": CATEGORIES}

@router.get("/featured")
def featured_businesses(db: Session = Depends(get_db)):
    businesses = list(db.scalars(select(Business).where(Business.featured.is_(True)).order_by(Business.created_at.desc())))
    return {"items": [serialize_business(db, business) for business in businesses]}
