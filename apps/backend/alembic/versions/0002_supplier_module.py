from __future__ import annotations
"""supplier module

Revision ID: 0002_supplier_module
Revises: 0001_initial
Create Date: 2026-05-21
"""

from alembic import op
import sqlalchemy as sa

revision = "0002_supplier_module"
down_revision = "0001_initial"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "suppliers",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(160), nullable=False),
        sa.Column("email", sa.String(255), nullable=True),
        sa.Column("status", sa.String(20), nullable=False, server_default="pending"),
        sa.Column("api_key_hash", sa.String(128), nullable=True),
        sa.Column("reward_percent", sa.Numeric(8, 4), nullable=False, server_default="70"),
        sa.Column("balance", sa.Numeric(12, 4), nullable=False, server_default="0"),
        sa.Column("held_balance", sa.Numeric(12, 4), nullable=False, server_default="0"),
        sa.Column("currency", sa.String(3), nullable=False, server_default="USD"),
        sa.Column("notes", sa.String(1000), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_suppliers_status", "suppliers", ["status"])
    op.create_index("ix_suppliers_api_key_hash", "suppliers", ["api_key_hash"], unique=True)

    op.create_table(
        "supplier_inventory",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("supplier_id", sa.Integer(), sa.ForeignKey("suppliers.id"), nullable=False),
        sa.Column("service_code", sa.String(50), nullable=False),
        sa.Column("country_iso2", sa.String(2), nullable=False),
        sa.Column("operator", sa.String(80), nullable=True),
        sa.Column("available_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("success_rate", sa.Numeric(5, 2), nullable=True),
        sa.Column("avg_sms_time_seconds", sa.Integer(), nullable=True),
        sa.Column("status", sa.String(20), nullable=False, server_default="active"),
        sa.Column("last_sync_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint(
            "supplier_id",
            "service_code",
            "country_iso2",
            "operator",
            name="uq_supplier_inventory_key",
        ),
    )
    op.create_index("ix_supplier_inventory_supplier_id", "supplier_inventory", ["supplier_id"])
    op.create_index("ix_supplier_inventory_service_code", "supplier_inventory", ["service_code"])
    op.create_index("ix_supplier_inventory_country_iso2", "supplier_inventory", ["country_iso2"])
    op.create_index("ix_supplier_inventory_status", "supplier_inventory", ["status"])

    op.create_table(
        "supplier_activations",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("supplier_id", sa.Integer(), sa.ForeignKey("suppliers.id"), nullable=False),
        sa.Column("order_id", sa.Integer(), sa.ForeignKey("orders.id"), nullable=True),
        sa.Column("supplier_activation_id", sa.String(120), nullable=True),
        sa.Column("phone_number", sa.String(40), nullable=False),
        sa.Column("service_code", sa.String(50), nullable=False),
        sa.Column("country_iso2", sa.String(2), nullable=False),
        sa.Column("operator", sa.String(80), nullable=True),
        sa.Column("status", sa.String(30), nullable=False, server_default="reserved"),
        sa.Column("client_price", sa.Numeric(12, 4), nullable=False),
        sa.Column("supplier_reward", sa.Numeric(12, 4), nullable=False),
        sa.Column("sms_text", sa.String(500), nullable=True),
        sa.Column("sms_code", sa.String(20), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("supplier_id", "supplier_activation_id", name="uq_supplier_activation_external_id"),
    )
    op.create_index("ix_supplier_activations_supplier_id", "supplier_activations", ["supplier_id"])
    op.create_index("ix_supplier_activations_order_id", "supplier_activations", ["order_id"], unique=True)
    op.create_index("ix_supplier_activations_supplier_activation_id", "supplier_activations", ["supplier_activation_id"])
    op.create_index("ix_supplier_activations_phone_number", "supplier_activations", ["phone_number"])
    op.create_index("ix_supplier_activations_service_code", "supplier_activations", ["service_code"])
    op.create_index("ix_supplier_activations_country_iso2", "supplier_activations", ["country_iso2"])
    op.create_index("ix_supplier_activations_status", "supplier_activations", ["status"])

    op.create_table(
        "supplier_sms",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("supplier_id", sa.Integer(), sa.ForeignKey("suppliers.id"), nullable=False),
        sa.Column("activation_id", sa.Integer(), sa.ForeignKey("supplier_activations.id"), nullable=True),
        sa.Column("order_id", sa.Integer(), sa.ForeignKey("orders.id"), nullable=True),
        sa.Column("supplier_sms_id", sa.String(120), nullable=False),
        sa.Column("phone_number", sa.String(40), nullable=False),
        sa.Column("phone_from", sa.String(120), nullable=True),
        sa.Column("text", sa.String(1000), nullable=False),
        sa.Column("status", sa.String(20), nullable=False, server_default="received"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("supplier_id", "supplier_sms_id", name="uq_supplier_sms_external_id"),
    )
    op.create_index("ix_supplier_sms_supplier_id", "supplier_sms", ["supplier_id"])
    op.create_index("ix_supplier_sms_activation_id", "supplier_sms", ["activation_id"])
    op.create_index("ix_supplier_sms_order_id", "supplier_sms", ["order_id"])
    op.create_index("ix_supplier_sms_phone_number", "supplier_sms", ["phone_number"])

    op.create_table(
        "supplier_transactions",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("supplier_id", sa.Integer(), sa.ForeignKey("suppliers.id"), nullable=False),
        sa.Column("activation_id", sa.Integer(), sa.ForeignKey("supplier_activations.id"), nullable=True),
        sa.Column("order_id", sa.Integer(), sa.ForeignKey("orders.id"), nullable=True),
        sa.Column("type", sa.String(20), nullable=False),
        sa.Column("amount", sa.Numeric(12, 4), nullable=False),
        sa.Column("status", sa.String(20), nullable=False, server_default="completed"),
        sa.Column("reference", sa.String(255), nullable=True),
        sa.Column("metadata", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("supplier_id", "order_id", "type", "status", name="uq_supplier_order_tx"),
    )
    op.create_index("ix_supplier_transactions_supplier_id", "supplier_transactions", ["supplier_id"])
    op.create_index("ix_supplier_transactions_activation_id", "supplier_transactions", ["activation_id"])
    op.create_index("ix_supplier_transactions_order_id", "supplier_transactions", ["order_id"])
    op.create_index("ix_supplier_transactions_type", "supplier_transactions", ["type"])


def downgrade() -> None:
    op.drop_table("supplier_transactions")
    op.drop_table("supplier_sms")
    op.drop_table("supplier_activations")
    op.drop_table("supplier_inventory")
    op.drop_table("suppliers")
