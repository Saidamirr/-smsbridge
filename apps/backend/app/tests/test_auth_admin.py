from __future__ import annotations
from sqlalchemy import select

from app.db.session import SessionLocal
from app.models import AuditLog, WalletTransaction


def test_user_registration_login(client):
    response = client.post("/auth/register", json={"email": "new@example.com", "password": "strong-pass", "locale": "en"})
    assert response.status_code == 200
    assert response.json()["user"]["status"] == "active"

    login = client.post("/auth/login", json={"email": "new@example.com", "password": "strong-pass"})
    assert login.status_code == 200
    assert login.json()["access_token"]


def test_admin_login_seed_account(client):
    response = client.post("/auth/login", json={"email": "admin@smsbridge.local", "password": "change-me"})
    assert response.status_code == 200, response.text
    assert response.json()["user"]["role"] == "admin"


def test_admin_manual_deposit(client, admin_token):
    response = client.post(
        "/admin/wallets/deposit",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={"user_id": 2, "amount": "10.00", "reference": "manual-test"},
    )
    assert response.status_code == 200, response.text
    assert response.json()["balance"] == "35.0000"
    db = SessionLocal()
    try:
        tx = db.scalar(select(WalletTransaction).where(WalletTransaction.type == "deposit", WalletTransaction.user_id == 2))
        audit = db.scalar(select(AuditLog).where(AuditLog.action == "wallet.deposit", AuditLog.entity_id == "2"))
        assert tx is not None
        assert audit is not None
    finally:
        db.close()


def test_normal_user_cannot_call_admin_deposit(client, user_token):
    response = client.post(
        "/admin/wallets/deposit",
        headers={"Authorization": f"Bearer {user_token}"},
        json={"user_id": 2, "amount": "10.00"},
    )
    assert response.status_code == 403


def test_admin_deposit_requires_valid_token(client):
    missing = client.post("/admin/wallets/deposit", json={"user_id": 2, "amount": "10.00"})
    assert missing.status_code == 401

    invalid = client.post(
        "/admin/wallets/deposit",
        headers={"Authorization": "Bearer not-a-real-token"},
        json={"user_id": 2, "amount": "10.00"},
    )
    assert invalid.status_code == 401
    assert invalid.json()["detail"] == "Invalid token"


def test_admin_can_update_user_limits(client, admin_token):
    response = client.patch(
        "/admin/users/2/limits",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={"max_orders_per_day": 50, "max_daily_spend": "100.00", "tier": "verified"},
    )
    assert response.status_code == 200, response.text
    body = response.json()
    assert body["tier"] == "verified"
    assert body["limit"]["max_orders_per_day"] == 50


def test_admin_metrics_return_basic_values(client, admin_token):
    response = client.get("/admin/metrics", headers={"Authorization": f"Bearer {admin_token}"})
    assert response.status_code == 200
    assert response.json()["total_users"] == 2
