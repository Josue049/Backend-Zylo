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
## Estructura del proyecto (resumen)

- `app/` — código del backend y rutas
- `app/routes/` — módulos por dominio (auth, users, services, bookings, etc.)
- `pyproject.toml` — dependencias y metadatos del proyecto
