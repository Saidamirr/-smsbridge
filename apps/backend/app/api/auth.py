from __future__ import annotations
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.deps import get_current_user
from app.core.security import create_token, decode_token, hash_password, verify_password
from app.db.session import get_db
from app.models import User, UserLimit, Wallet
from app.schemas.auth import AuthOut, LoginIn, RefreshIn, RegisterIn, TokenOut
from app.schemas.common import UserPublic

router = APIRouter(prefix="/auth", tags=["auth"])


def _tokens(user: User) -> TokenOut:
    return TokenOut(
        access_token=create_token(str(user.id), settings.access_token_minutes, "access"),
        refresh_token=create_token(str(user.id), settings.refresh_token_minutes, "refresh"),
    )


@router.post("/register", response_model=AuthOut)
def register(payload: RegisterIn, db: Session = Depends(get_db)):
    existing = db.scalar(select(User).where(User.email == payload.email.lower()))
    if existing:
        raise HTTPException(status_code=409, detail="Email is already registered")
    user = User(email=payload.email.lower(), password_hash=hash_password(payload.password), locale=payload.locale)
    user.limit = UserLimit()
    user.wallet = Wallet()
    db.add(user)
    db.commit()
    db.refresh(user)
    token = _tokens(user)
    return AuthOut(**token.model_dump(), user=UserPublic.model_validate(user))


@router.post("/login", response_model=AuthOut)
def login(payload: LoginIn, db: Session = Depends(get_db)):
    user = db.scalar(select(User).where(User.email == payload.email.lower()))
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")
    token = _tokens(user)
    return AuthOut(**token.model_dump(), user=UserPublic.model_validate(user))


@router.post("/refresh", response_model=TokenOut)
def refresh(payload: RefreshIn, db: Session = Depends(get_db)):
    decoded = decode_token(payload.refresh_token)
    if not decoded or decoded.get("typ") != "refresh":
        raise HTTPException(status_code=401, detail="Invalid refresh token")
    user = db.get(User, int(decoded["sub"]))
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return _tokens(user)


@router.get("/me", response_model=UserPublic)
def me(user: User = Depends(get_current_user)):
    return user

