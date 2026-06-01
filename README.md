# Backend Zylo

Resumen del backend de Zylo: una API en Python diseñada para manejar usuarios, negocios, servicios y reservas, con endpoints organizados en `app/routes/`.

**Proyecto para UTP 2026 - Segundo avance**
**Curso:** Herramientas de desarrollo

**Tecnologías principales:** Python, FastAPI

## Características
- Gestión de usuarios (registro, autenticación, perfiles)
- Gestión de negocios y servicios
- Reservas y notificaciones
- Sistema de chat entre clientes y empresas
- Reviews de empresas
- Estadisticas de empresas
- API modular con rutas en `app/routes/`

## Requisitos
- Python 3.11+ recomendado
- Despliegue en Vercel

## Ejecutar la aplicación en local

Requiere instalación de librerias previamente

```bash
uvicorn app.main:app --reload
```

## Recuperación de contraseña por correo

El endpoint `/auth/forgot-password` envía el token por SMTP usando `fastapi-mail`.

Variables necesarias en el entorno:

- `MAIL_SERVER` = `smtp.gmail.com`
- `MAIL_PORT` = `587`
- `MAIL_USERNAME` = tu correo de Gmail
- `MAIL_PASSWORD` = tu app password de Gmail
- `MAIL_FROM` = opcional, si no se define se usa `MAIL_USERNAME`
- `MAIL_FROM_NAME` opcional
- `MAIL_STARTTLS` opcional
- `MAIL_SSL_TLS` opcional
- `MAIL_USE_CREDENTIALS` opcional
- `MAIL_VALIDATE_CERTS` opcional

Importante: Gmail no acepta tu contraseña normal para SMTP. Debes crear una app password en tu cuenta de Google y usarla en `MAIL_PASSWORD`.

## Estructura del proyecto (resumen)

- `app/` — código del backend y rutas
- `app/routes/` — módulos por dominio (auth, users, services, bookings, etc.)
- `pyproject.toml` — dependencias y metadatos del proyecto
