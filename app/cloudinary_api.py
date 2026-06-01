from __future__ import annotations

import hashlib
import httpx

def upload_image_bytes(
    *,
    cloud_name: str,
    folder: str,
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
