from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.deps import get_current_supplier, require_active_supplier
from app.db.session import get_db
from app.models import Supplier, SupplierInventory
from app.schemas.supplier import (
    SupplierInventoryOut,
    SupplierInventoryUpdateIn,
    SupplierInventoryUpdateOut,
    SupplierMeOut,
    SupplierSmsIn,
    SupplierSmsPushOut,
)
from app.services.suppliers import push_sms, upsert_inventory

router = APIRouter(prefix="/supplier/v1", tags=["supplier-api"])


@router.get("/me", response_model=SupplierMeOut)
def me(supplier: Supplier = Depends(get_current_supplier)):
    return supplier


@router.get("/inventory", response_model=list[SupplierInventoryOut])
def inventory(db: Session = Depends(get_db), supplier: Supplier = Depends(get_current_supplier)):
    return list(
        db.scalars(
            select(SupplierInventory)
            .where(SupplierInventory.supplier_id == supplier.id)
            .order_by(SupplierInventory.updated_at.desc())
        )
    )


@router.post("/inventory/update", response_model=SupplierInventoryUpdateOut)
def inventory_update(
    payload: SupplierInventoryUpdateIn,
    db: Session = Depends(get_db),
    supplier: Supplier = Depends(require_active_supplier),
):
    updated = upsert_inventory(db, supplier, payload.items)
    db.commit()
    return SupplierInventoryUpdateOut(updated=updated)


@router.post("/sms", response_model=SupplierSmsPushOut)
def sms_push(
    payload: SupplierSmsIn,
    db: Session = Depends(get_db),
    supplier: Supplier = Depends(require_active_supplier),
):
    _sms, duplicate = push_sms(db, supplier, payload)
    db.commit()
    return SupplierSmsPushOut(duplicate=duplicate)
