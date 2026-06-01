from __future__ import annotations

import hashlib
import time
from typing import Any

import httpx

def upload_image_bytes(
    *,
    cloud_name: str,
    api_key: str,
    api_secret: str,
    folder: str,
    file_name: str,
    file_bytes: bytes,
    content_type: str | None,
    public_id: str,
    timeout_seconds: float = 15.0,
) -> dict[str, Any]:
    endpoint = f"https://api.cloudinary.com/v1_1/{cloud_name}/image/upload"
    params_to_sign = {
        "folder": folder,
        "public_id": public_id,
        "timestamp": str(int(time.time())),
        "overwrite": "true",
    }
    signature = _signature(params_to_sign, api_secret)
    return payload
