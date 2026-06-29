from __future__ import annotations

from datetime import datetime, timedelta, timezone

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from .models import Booking, Business, Favorite, Notification, PasswordResetToken, Service, SessionToken, User
from .security import hash_password
from .utils import make_id


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


def seed_demo_data(db: Session) -> None:
    if db.scalar(select(func.count()).select_from(User)):
        return

    business_owner = User(
        id=make_id("user"),
        name="Demo Business",
        email="business@zylo.test",
        password_hash=hash_password("Demo1234!"),
        phone="+1 555 0100",
        location="Centro",
        role="business_owner",
    )
    client = User(
        id=make_id("user"),
        name="Demo Client",
        email="client@zylo.test",
        password_hash=hash_password("Demo1234!"),
        phone="+1 555 0110",
        location="Norte",
        role="client",
    )
    db.add_all([business_owner, client])
    db.flush()

    # Crear negocios que coincidan con los del frontend
    business1 = Business(
        id="1",
        owner_user_id=business_owner.id,
        name="The Serene Sanctuary",
        category_id="salon",
        description="Servicios premium de spa y bienestar con reserva online.",
        phone="+1 555 0100",
        email="serene@zylo.com",
        address="Av. Larco 1301, Miraflores, Lima, Perú",
        city="Lima",
        featured=True,
        availability_status=True,
        rating=4.9,
        reviews_count=120,
        image_url="https://images.unsplash.com/photo-1544161515-4ab6ce6db874?q=80&w=800",
        team=[{"id": make_id("member"), "name": "Ana", "role": "Terapeuta"}],
        gallery=[
            "https://images.unsplash.com/photo-1519014816548-bf5fe059798b?auto=format&fit=crop&w=1200&q=80",
            "https://images.unsplash.com/photo-1521590832167-7bcbfaa6381f?auto=format&fit=crop&w=1200&q=80",
            "https://images.unsplash.com/photo-1516733725519-9ec98d8b63b9?auto=format&fit=crop&w=1200&q=80",
            "https://images.unsplash.com/photo-1567722715463-84d440642117?auto=format&fit=crop&w=1200&q=80",
        ],
        weekly_hours={
            "monday": ["09:00", "18:00"],
            "tuesday": ["09:00", "18:00"],
            "wednesday": ["09:00", "18:00"],
            "thursday": ["09:00", "18:00"],
            "friday": ["09:00", "18:00"],
            "saturday": ["10:00", "15:00"],
            "sunday": [],
        },
    )
    
    business2 = Business(
        id="2",
        owner_user_id=business_owner.id,
        name="Urban Wellness Hub",
        category_id="salon",
        description="Centro de bienestar urbano con servicios innovadores.",
        phone="+1 555 0101",
        email="urban@zylo.com",
        address="Centro Comercial Plaza Mayor",
        city="Lima",
        featured=True,
        availability_status=True,
        rating=4.7,
        reviews_count=95,
        image_url="https://images.unsplash.com/photo-1599643478518-a784e5dc4c8f?q=80&w=800",
        team=[{"id": make_id("member"), "name": "Carlos", "role": "Entrenador"}],
        gallery=[
            "https://images.unsplash.com/photo-1534438327276-14e5300c3a48?auto=format&fit=crop&w=1200&q=80",
            "https://images.unsplash.com/photo-1521286753344-2be0d552e25b?auto=format&fit=crop&w=1200&q=80",
            "https://images.unsplash.com/photo-1529156069898-49953e39b3ac?auto=format&fit=crop&w=1200&q=80",
            "https://images.unsplash.com/photo-1578762996442-48f60103fc96?auto=format&fit=crop&w=1200&q=80",
        ],
        weekly_hours={
            "monday": ["06:00", "21:00"],
            "tuesday": ["06:00", "21:00"],
            "wednesday": ["06:00", "21:00"],
            "thursday": ["06:00", "21:00"],
            "friday": ["06:00", "21:00"],
            "saturday": ["08:00", "20:00"],
            "sunday": ["08:00", "18:00"],
        },
    )
    
    db.add_all([business1, business2])
    db.flush()

    business_owner.business_id = business1.id

    db.add_all(
        [
            Service(
                id=make_id("srv"),
                business_id="1",
                name="Masaje Relajante",
                description="Masaje relajante de cuerpo completo.",
                duration_minutes=60,
                price=60.0,
                active=True,
                weekly_hours={
                    "monday": ["09:00", "18:00"],
                    "tuesday": ["09:00", "18:00"],
                    "wednesday": ["09:00", "18:00"],
                    "thursday": ["09:00", "18:00"],
                    "friday": ["09:00", "18:00"],
                    "saturday": ["10:00", "15:00"],
                    "sunday": [],
                },
                professionals=[
                    {"id": "ana", "name": "Ana", "role": "Terapeuta"},
                ],
            ),
            Service(
                id=make_id("srv"),
                business_id="2",
                name="Entrenamiento Personal",
                description="Sesión de entrenamiento personalizado.",
                duration_minutes=60,
                price=80.0,
                active=True,
                weekly_hours={
                    "monday": ["06:00", "21:00"],
                    "tuesday": ["06:00", "21:00"],
                    "wednesday": ["06:00", "21:00"],
                    "thursday": ["06:00", "21:00"],
                    "friday": ["06:00", "21:00"],
                    "saturday": ["08:00", "20:00"],
                    "sunday": ["08:00", "18:00"],
                },
                professionals=[
                    {"id": "carlos", "name": "Carlos", "role": "Entrenador"},
                ],
            ),
            Favorite(user_id=client.id, business_id="1"),
            SessionToken(token="demo-internal-token", user_id=client.id, last_seen_at=utcnow()),
            PasswordResetToken(token="demo-reset-token", user_id=client.id, expires_at=utcnow() + timedelta(hours=1)),
        ]
    )
    db.commit()
