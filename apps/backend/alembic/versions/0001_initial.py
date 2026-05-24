from __future__ import annotations
"""initial schema

Revision ID: 0001_initial
Revises:
Create Date: 2026-05-18
"""

from alembic import op
import sqlalchemy as sa

revision = "0001_initial"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("email", sa.String(255), nullable=False),
        sa.Column("password_hash", sa.String(255), nullable=False),
        sa.Column("role", sa.String(20), nullable=False, server_default="user"),
        sa.Column("status", sa.String(20), nullable=False, server_default="active"),
        sa.Column("tier", sa.String(20), nullable=False, server_default="default"),
        sa.Column("api_key_hash", sa.String(128), nullable=True),
        sa.Column("locale", sa.String(2), nullable=False, server_default="en"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_users_email", "users", ["email"], unique=True)
    op.create_index("ix_users_api_key_hash", "users", ["api_key_hash"], unique=True)

    op.create_table(
        "user_limits",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False, unique=True),
        sa.Column("max_orders_per_minute", sa.Integer(), nullable=False, server_default="3"),
        sa.Column("max_orders_per_day", sa.Integer(), nullable=False, server_default="20"),
        sa.Column("max_active_orders", sa.Integer(), nullable=False, server_default="3"),
        sa.Column("max_daily_spend", sa.Numeric(12, 4), nullable=False, server_default="10"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_table(
        "wallets",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False, unique=True),
        sa.Column("balance", sa.Numeric(12, 4), nullable=False, server_default="0"),
        sa.Column("held_balance", sa.Numeric(12, 4), nullable=False, server_default="0"),
        sa.Column("currency", sa.String(3), nullable=False, server_default="USD"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_table(
        "providers",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(120), nullable=False),
        sa.Column("code", sa.String(50), nullable=False),
        sa.Column("type", sa.String(20), nullable=False, server_default="mock"),
        sa.Column("status", sa.String(20), nullable=False, server_default="active"),
        sa.Column("priority", sa.Integer(), nullable=False, server_default="100"),
        sa.Column("base_url", sa.String(500), nullable=True),
        sa.Column("api_key_encrypted", sa.String(500), nullable=True),
        sa.Column("default_markup_percent", sa.Numeric(8, 4), nullable=False, server_default="25"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_providers_code", "providers", ["code"], unique=True)
    op.create_table(
        "services",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("code", sa.String(50), nullable=False),
        sa.Column("name_ru", sa.String(120), nullable=False),
        sa.Column("name_en", sa.String(120), nullable=False),
        sa.Column("category", sa.String(120), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_services_code", "services", ["code"], unique=True)
    op.create_table(
        "countries",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("iso2", sa.String(2), nullable=False),
        sa.Column("name_ru", sa.String(120), nullable=False),
        sa.Column("name_en", sa.String(120), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_countries_iso2", "countries", ["iso2"], unique=True)
    op.create_table(
        "prices",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("provider_id", sa.Integer(), sa.ForeignKey("providers.id"), nullable=False),
        sa.Column("service_code", sa.String(50), nullable=False),
        sa.Column("country_iso2", sa.String(2), nullable=False),
        sa.Column("operator", sa.String(80), nullable=True),
        sa.Column("provider_cost", sa.Numeric(12, 4), nullable=False),
        sa.Column("final_price", sa.Numeric(12, 4), nullable=False),
        sa.Column("available_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("delivery_rate", sa.Numeric(5, 2), nullable=False, server_default="90"),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("provider_id", "service_code", "country_iso2", "operator", name="uq_provider_price"),
    )
    op.create_index("ix_prices_provider_id", "prices", ["provider_id"])
    op.create_index("ix_prices_service_code", "prices", ["service_code"])
    op.create_index("ix_prices_country_iso2", "prices", ["country_iso2"])
    op.create_table(
        "orders",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("public_id", sa.String(36), nullable=False),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("provider_id", sa.Integer(), sa.ForeignKey("providers.id"), nullable=False),
        sa.Column("provider_order_id", sa.String(120), nullable=True),
        sa.Column("service_code", sa.String(50), nullable=False),
        sa.Column("country_iso2", sa.String(2), nullable=False),
        sa.Column("operator", sa.String(80), nullable=True),
        sa.Column("phone_number", sa.String(40), nullable=True),
        sa.Column("status", sa.String(30), nullable=False, server_default="created"),
        sa.Column("price", sa.Numeric(12, 4), nullable=False),
        sa.Column("provider_cost", sa.Numeric(12, 4), nullable=False),
        sa.Column("sms_code", sa.String(20), nullable=True),
        sa.Column("sms_text", sa.String(500), nullable=True),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_orders_public_id", "orders", ["public_id"], unique=True)
    op.create_index("ix_orders_user_id", "orders", ["user_id"])
    op.create_index("ix_orders_provider_id", "orders", ["provider_id"])
    op.create_index("ix_orders_status", "orders", ["status"])
    op.create_index("ix_orders_service_code", "orders", ["service_code"])
    op.create_index("ix_orders_country_iso2", "orders", ["country_iso2"])
    op.create_table(
        "wallet_transactions",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("order_id", sa.Integer(), sa.ForeignKey("orders.id"), nullable=True),
        sa.Column("type", sa.String(20), nullable=False),
        sa.Column("amount", sa.Numeric(12, 4), nullable=False),
        sa.Column("status", sa.String(20), nullable=False, server_default="completed"),
        sa.Column("reference", sa.String(255), nullable=True),
        sa.Column("metadata", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("order_id", "type", "status", name="uq_wallet_order_type_status"),
    )
    op.create_index("ix_wallet_transactions_user_id", "wallet_transactions", ["user_id"])
    op.create_index("ix_wallet_transactions_order_id", "wallet_transactions", ["order_id"])
    op.create_index("ix_wallet_transactions_type", "wallet_transactions", ["type"])
    op.create_table(
        "audit_logs",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("actor_user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=True),
        sa.Column("action", sa.String(120), nullable=False),
        sa.Column("entity_type", sa.String(80), nullable=False),
        sa.Column("entity_id", sa.String(120), nullable=True),
        sa.Column("metadata", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_audit_logs_action", "audit_logs", ["action"])
    op.create_table(
        "api_request_logs",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=True),
        sa.Column("endpoint", sa.String(500), nullable=False),
        sa.Column("method", sa.String(10), nullable=False),
        sa.Column("ip_address", sa.String(80), nullable=True),
        sa.Column("status_code", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_api_request_logs_user_id", "api_request_logs", ["user_id"])
    op.create_table(
        "system_settings",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("key", sa.String(120), nullable=False),
        sa.Column("value", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_system_settings_key", "system_settings", ["key"], unique=True)


def downgrade() -> None:
    for table in [
        "system_settings",
        "api_request_logs",
        "audit_logs",
        "wallet_transactions",
        "orders",
        "prices",
        "countries",
        "services",
        "providers",
        "wallets",
        "user_limits",
        "users",
    ]:
        op.drop_table(table)

