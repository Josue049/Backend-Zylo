from __future__ import annotations

from collections.abc import Mapping

from fastapi import Depends, HTTPException, Request, Security, status
from fastapi.security import APIKeyHeader
from sqlalchemy import select
from sqlalchemy.orm import Session
from datetime import datetime, timezone

from .db import get_db
from .models import Business, SessionToken, User


authorization_key = APIKeyHeader(name="Authorization", auto_error=False)


def _normalize_session_token(value: str | None) -> str | None:
    token = value.strip().strip('"').strip("'")
    lowered = token.lower()
    for prefix in ("bearer ", "token ", "jwt "):
        if lowered.startswith(prefix):
            token = token.split(" ", 1)[1].strip()
            break
    return token or None
