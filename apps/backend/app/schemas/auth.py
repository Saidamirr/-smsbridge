from __future__ import annotations
from pydantic import BaseModel, Field

from app.schemas.common import UserPublic


class RegisterIn(BaseModel):
    email: str = Field(min_length=3, max_length=255)
    password: str = Field(min_length=8, max_length=128)
    locale: str = Field(default="en", pattern="^(en|ru)$")


class LoginIn(BaseModel):
    email: str = Field(min_length=3, max_length=255)
    password: str


class TokenOut(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class AuthOut(TokenOut):
    user: UserPublic


class RefreshIn(BaseModel):
    refresh_token: str
