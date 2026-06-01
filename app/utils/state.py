from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from threading import Lock
from typing import Any
from uuid import uuid4

from .security import create_reset_token, create_session_token, hash_password, verify_password

def utcnow() -> datetime:
    return datetime.now(timezone.utc)

def make_id(prefix: str) -> str:
    return f"{prefix}_{uuid4().hex[:12]}"

@dataclass
class AppState:
    lock: Lock = field(default_factory=Lock)
    users: dict[str, dict[str, Any]] = field(default_factory=dict)
    sessions: dict[str, dict[str, Any]] = field(default_factory=dict)
    businesses: dict[str, dict[str, Any]] = field(default_factory=dict)
    services: dict[str, dict[str, Any]] = field(default_factory=dict)
    bookings: dict[str, dict[str, Any]] = field(default_factory=dict)
    availability_blocks: dict[str, dict[str, Any]] = field(default_factory=dict)
    favorites: dict[str, set[str]] = field(default_factory=lambda: defaultdict(set))
    conversations: dict[str, dict[str, Any]] = field(default_factory=dict)
    messages: dict[str, dict[str, Any]] = field(default_factory=dict)
    notifications: dict[str, dict[str, Any]] = field(default_factory=dict)
    password_reset_tokens: dict[str, dict[str, Any]] = field(default_factory=dict)
    categories: list[dict[str, str]] = field(default_factory=list)
    