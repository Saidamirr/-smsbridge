from __future__ import annotations
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.models import AuditLog


def add_audit_log(
    db: Session,
    action: str,
    entity_type: str,
    entity_id: str | None = None,
    actor_user_id: int | None = None,
    metadata: dict | None = None,
) -> None:
    db.add(
        AuditLog(
            actor_user_id=actor_user_id,
            action=action,
            entity_type=entity_type,
            entity_id=entity_id,
            log_metadata=jsonable_encoder(metadata or {}),
        )
    )
