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

    @dataclass
class AppState:
    lock: Lock = field(default_factory=Lock)
    # ... (todos los campos del commit 1)
    
    def __post_init__(self) -> None:
        self._seed()

    def _seed(self) -> None:
        self.categories = [
            {"id": "salon", "name": "Salón"},
            {"id": "spa", "name": "Spa"},
            {"id": "barber", "name": "Barbería"},
            {"id": "fitness", "name": "Fitness"},
        ]

        business_owner = self.create_user(
            {
                "name": "Demo Business",
                "email": "business@zylo.test",
                "password": "Demo1234!",
                "phone": "+1 555 0100",
                "location": "Centro",
                "role": "business_owner",
            }
        )
        client = self.create_user(
            {
                "name": "Demo Client",
                "email": "client@zylo.test",
                "password": "Demo1234!",
                "phone": "+1 555 0110",
                "location": "Norte",
                "role": "client",
            }
        )

        business = self.create_business(
            owner_user_id=business_owner["id"],
            payload={
                "name": "Zylo Studio",
                "category_id": "salon",
                "description": "Servicios premium con reserva online.",
                "phone": "+1 555 0100",
                "address": "Av. Principal 123",
                "city": "Ciudad Central",
                "featured": True,
                "availability_status": True,
                "team": [
                    {"id": make_id("member"), "name": "Ana", "role": "Estilista"},
                    {"id": make_id("member"), "name": "Luis", "role": "Barbero"},
                ],
                "gallery": [
                    {"id": make_id("img"), "url": "https://images.unsplash.com/photo-1519014816548-bf5fe059798b?auto=format&fit=crop&w=1200&q=80", "alt": "Interior"},
                    {"id": make_id("img"), "url": "https://images.unsplash.com/photo-1521590832167-7bcbfaa6381f?auto=format&fit=crop&w=1200&q=80", "alt": "Equipo"},
                ],
            },
        )

        self.add_service(
            business["id"],
            {
                "name": "Corte de cabello",
                "description": "Corte profesional y lavado.",
                "duration_minutes": 45,
                "price": 18.0,
                "active": True,
            },
        )
        self.add_service(
            business["id"],
            {
                "name": "Barba",
                "description": "Perfilado y acabado.",
                "duration_minutes": 30,
                "price": 12.0,
                "active": True,
            },
        )

        self.favorites[client["id"]].add(business["id"])