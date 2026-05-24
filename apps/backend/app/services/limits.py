from __future__ import annotations
from datetime import datetime, timedelta, timezone
from decimal import Decimal

from fastapi import HTTPException
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models import Order, User, WalletTransaction
from app.core.errors import api_error

ACTIVE_ORDER_STATUSES = {"created", "reserved", "waiting_sms", "sms_received"}

TIER_LIMITS = {
    "default": {
        "max_orders_per_minute": 3,
        "max_orders_per_day": 20,
        "max_active_orders": 3,
        "max_daily_spend": Decimal("10.00"),
    },
    "verified": {
        "max_orders_per_minute": 10,
        "max_orders_per_day": 200,
        "max_active_orders": 20,
        "max_daily_spend": Decimal("100.00"),
    },
    "wholesale": {
        "max_orders_per_minute": 60,
        "max_orders_per_day": 5000,
        "max_active_orders": 500,
        "max_daily_spend": Decimal("5000.00"),
    },
    "partner": {
        "max_orders_per_minute": 300,
        "max_orders_per_day": 50000,
        "max_active_orders": 5000,
        "max_daily_spend": Decimal("50000.00"),
    },
}


def apply_tier_limits(user: User, tier: str) -> None:
    if not user.limit or tier not in TIER_LIMITS:
        return
    for key, value in TIER_LIMITS[tier].items():
        setattr(user.limit, key, value)


def enforce_can_order(db: Session, user: User, price: Decimal) -> None:
    if user.status == "blocked":
        raise api_error(403, "FORBIDDEN", "Blocked users cannot create orders")
    if user.status not in {"active", "limited"}:
        raise HTTPException(status_code=403, detail="User status does not allow orders")
    if not user.limit:
        raise HTTPException(status_code=403, detail="User limits are not configured")

    now = datetime.now(timezone.utc)
    one_minute = now - timedelta(minutes=1)
    start_of_day = now.replace(hour=0, minute=0, second=0, microsecond=0)

    orders_last_minute = db.scalar(
        select(func.count(Order.id)).where(Order.user_id == user.id, Order.created_at >= one_minute)
    )
    if orders_last_minute >= user.limit.max_orders_per_minute:
        raise api_error(429, "DAILY_LIMIT_EXCEEDED", "Orders per minute limit exceeded")

    orders_today = db.scalar(
        select(func.count(Order.id)).where(Order.user_id == user.id, Order.created_at >= start_of_day)
    )
    if orders_today >= user.limit.max_orders_per_day:
        raise api_error(429, "DAILY_LIMIT_EXCEEDED", "Daily order limit exceeded")

    active_orders = db.scalar(
        select(func.count(Order.id)).where(Order.user_id == user.id, Order.status.in_(ACTIVE_ORDER_STATUSES))
    )
    if active_orders >= user.limit.max_active_orders:
        raise api_error(429, "ACTIVE_ORDER_LIMIT_EXCEEDED", "Active order limit exceeded")

    spent_today = db.scalar(
        select(func.coalesce(func.sum(WalletTransaction.amount), 0)).where(
            WalletTransaction.user_id == user.id,
            WalletTransaction.type == "hold",
            WalletTransaction.status == "completed",
            WalletTransaction.created_at >= start_of_day,
        )
    )
    if Decimal(str(spent_today)) + price > user.limit.max_daily_spend:
        raise api_error(429, "DAILY_LIMIT_EXCEEDED", "Daily spend limit exceeded")
