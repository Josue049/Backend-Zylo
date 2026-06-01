from __future__ import annotations

from fastapi import HTTPException, status
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType

from .db import settings


def _build_mail_config() -> ConnectionConfig:
    required_values = {
        "mail_server": settings.mail_server,
        "mail_port": settings.mail_port,
        "mail_username": settings.mail_username,
        "mail_password": settings.mail_password,
        "mail_from": settings.mail_from,
    }
    missing_fields = [name for name, value in required_values.items() if value in {None, ""}]
    if missing_fields:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Email service is not configured",
        )

    return ConnectionConfig(
        MAIL_SERVER=settings.mail_server,
        MAIL_PORT=settings.mail_port,
        MAIL_USERNAME=settings.mail_username,
        MAIL_PASSWORD=settings.mail_password,
        MAIL_FROM=settings.mail_from,
        MAIL_FROM_NAME=settings.mail_from_name,
        MAIL_STARTTLS=settings.mail_starttls,
        MAIL_SSL_TLS=settings.mail_ssl_tls,
        USE_CREDENTIALS=settings.mail_use_credentials,
        VALIDATE_CERTS=settings.mail_validate_certs,
    )


async def send_password_reset_email(recipient_email: str, reset_token: str) -> None:
    message = MessageSchema(
        subject="Recuperación de contraseña",
        recipients=[recipient_email],
        body=(
            f"Hola,\n\n"
            f"Tu token de recuperación es: {reset_token}\n\n"
            f"Usa este token en el formulario de restablecimiento de contraseña.\n"
            f"Si no solicitaste este cambio, ignora este mensaje."
        ),
        subtype=MessageType.plain,
    )
    mailer = FastMail(_build_mail_config())
    await mailer.send_message(message)

    