from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..db import get_db
from ..deps import get_current_business, get_current_user
from ..models import Booking, Business, Notification, Service, User
from ..schemas import BookingCreateRequest, BookingRescheduleRequest, BookingStatusRequest
from ..serializers import booking_payload
from ..utils import make_id
from .businesses import check_business_availability_for_booking, service_allows_slot

router = APIRouter(prefix="/bookings", tags=["bookings"])

