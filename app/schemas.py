from __future__ import annotations

from typing import Literal, Optional

from pydantic import BaseModel, Field

AccountType = Literal["user", "business"]


class RegisterRequest(BaseModel):
    account_type: AccountType = Field(default="user")
    name: str
    email: str
    password: str
    phone: Optional[str] = None
    location: Optional[str] = None
    business_name: Optional[str] = None
    category_id: Optional[str] = None
    description: Optional[str] = None


class LoginRequest(BaseModel):
    email: str
    password: str


class ForgotPasswordRequest(BaseModel):
    email: str


class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str