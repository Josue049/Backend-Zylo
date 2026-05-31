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


