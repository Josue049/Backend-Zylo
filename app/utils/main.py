from __future__ import annotations

import sys
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import inspect, text

@app.get("/")
def healthcheck():
    return {"status": "ok", "service": "Zylo API", "docs": "/docs"}