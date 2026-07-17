from __future__ import annotations

from collections.abc import Iterable

from sqlalchemy import select
from sqlalchemy.orm import Session

from .models import Booking, Business, Conversation, Favorite, Message, Notification, Review, Service, User

STATUS_TRANSLATIONS = {
    "pending": "Pendiente",
    "accepted": "Aceptada",
    "rejected": "Rechazada",
    "canceled": "Cancelada",
    "cancelled": "Cancelada",
    "completed": "Completada",
}

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


def business_payload(business: Business, services_count: int = 0, active_services_count: int = 0, category_name: str | None = None) -> dict:
    gallery = business.gallery or []
    image_url = business.image_url.strip() if isinstance(business.image_url, str) and business.image_url.strip() else None
    if not image_url and gallery:
        image_url = gallery[0]
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
        "image_url": image_url,
        "team": business.team or [],
        "gallery": business.gallery or [],
        "weekly_hours": business.weekly_hours or {},
        "services_count": services_count,
        "active_services_count": active_services_count,
        "created_at": business.created_at,
        "updated_at": business.updated_at,
    }


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


def review_payload(review: Review, db: Session) -> dict:
    user = db.get(User, review.user_id)
    return {
        "id": review.id,
        "user_id": review.user_id,
        "user_name": None if not user else user.name,
        "user_email": None if not user else user.email,
        "user_photo": None if not user else user.photo_url,
        "business_id": review.business_id,
        "rating": review.rating,
        "comment": review.comment,
        "created_at": review.created_at,
        "updated_at": review.updated_at,
    }


# def booking_payload(booking: Booking, db: Session) -> dict:
#     business = db.get(Business, booking.business_id)
#     service = db.get(Service, booking.service_id)
#     user = db.get(User, booking.user_id)
#     return {
#         "id": booking.id,
#         "user_id": booking.user_id,
#         "business_id": booking.business_id,
#         "service_id": booking.service_id,
#         "professional_id": booking.professional_id,
#         "start_at": booking.start_at,
#         "end_at": booking.end_at,
#         "notes": booking.notes,
#         "status": booking.status,
#         "price": booking.price,
#         "created_at": booking.created_at,
#         "updated_at": booking.updated_at,
#         "business": None if not business else {"id": business.id, "name": business.name, "category_id": business.category_id},
#         "service": None if not service else {"id": service.id, "name": service.name, "duration_minutes": service.duration_minutes, "price": service.price},
#         "user": None if not user else {"id": user.id, "name": user.name, "email": user.email},
#     }

def booking_payload(booking: Booking, db: Session) -> dict:
    business = db.get(Business, booking.business_id)
    service = db.get(Service, booking.service_id)
    user = db.get(User, booking.user_id)
    
    # 1. Resolver el Profesional asignado (que es un Usuario)
    professional = db.get(User, booking.professional_id) if booking.professional_id else None
    professional_name = professional.name if professional else "Profesional no asignado"

    # 2. Resolver la imagen del negocio (imagen principal o primera de la galería)
    business_image_url = None
    if business:
        business_image_url = business.image_url.strip() if isinstance(business.image_url, str) and business.image_url.strip() else None
        if not business_image_url and business.gallery:
            business_image_url = business.gallery[0]

    return {
        "id": booking.id,
        "user_id": booking.user_id,
        "business_id": booking.business_id,
        "service_id": booking.service_id,
        "professional_id": booking.professional_id,
        "start_at": booking.start_at,
        "end_at": booking.end_at,
        "notes": booking.notes,
        "status": STATUS_TRANSLATIONS.get(
            booking.status.lower() if booking.status else "",
            booking.status,
        ),
        "price": booking.price,
        "created_at": booking.created_at,
        "updated_at": booking.updated_at,
        
        # ─── CAMPOS PLANOS PARA TU FRONTEND (REQUERIDOS EN BOOKINGS.TSX) ───
        "business_name": None if not business else business.name,
        "business_image_url": business_image_url,
        "service_name": None if not service else service.name,
        "professional_name": professional_name,
        
        # ─── OBJETOS ANIDADOS (MANTENIDOS POR COMPATIBILIDAD) ───
        "business": None if not business else {
            "id": business.id, 
            "name": business.name, 
            "category_id": business.category_id,
            "image_url": business_image_url
        },
        "service": None if not service else {
            "id": service.id, 
            "name": service.name, 
            "duration_minutes": service.duration_minutes, 
            "price": service.price
        },
        "user": None if not user else {
            "id": user.id, 
            "name": user.name, 
            "email": user.email
        },
    }

def conversation_payload(conversation: Conversation, db: Session, current_user: User) -> dict:
    messages = list(db.scalars(select(Message).where(Message.conversation_id == conversation.id).order_by(Message.created_at.asc())))
    user = db.get(User, conversation.user_id)
    business = db.get(Business, conversation.business_id)
    read_marker = conversation.last_read_at_business if current_user.role == "business_owner" else conversation.last_read_at_client
    unread = len([message for message in messages if message.sender_user_id != current_user.id and message.created_at > read_marker])
    
    # Get business photo from image_url or first gallery image
    business_photo = None
    if business:
        business_photo = business.image_url or (business.gallery[0] if business.gallery else None)
    
    return {
        "id": conversation.id,
        "user_id": conversation.user_id,
        "user_name": None if not user else user.name,
        "user_photo": None if not user else user.photo_url,
        "user_email": None if not user else user.email,
        "business_id": conversation.business_id,
        "business_name": None if not business else business.name,
        "business_category": None if not business else business.category_id,
        "business_photo": business_photo,
        "subject": conversation.subject,
        "last_read_at_client": conversation.last_read_at_client,
        "last_read_at_business": conversation.last_read_at_business,
        "created_at": conversation.created_at,
        "updated_at": conversation.updated_at,
        "messages_count": len(messages),
        "unread_count": unread,
        "last_message": None if not messages else message_payload(messages[-1]),
    }


def message_payload(message: Message, db: Session | None = None) -> dict:
    sender = db.get(User, message.sender_user_id) if db else None
    return {
        "id": message.id,
        "conversation_id": message.conversation_id,
        "sender_user_id": message.sender_user_id,
        "sender_name": None if not sender else sender.name,
        "sender_photo": None if not sender else sender.photo_url,
        "content": message.content,
        "text": message.content,
        "created_at": message.created_at,
        "timestamp": message.created_at,
    }


def notification_payload(notification: Notification) -> dict:
    return {
        "id": notification.id,
        "recipient_user_id": notification.recipient_user_id,
        "type": notification.type,
        "title": notification.title,
        "message": notification.message,
        "read": notification.read,
        "read_at": notification.read_at,
        "created_at": notification.created_at,
    }
