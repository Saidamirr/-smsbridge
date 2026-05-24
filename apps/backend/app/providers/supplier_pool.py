from __future__ import annotations

from app.providers.base import ProviderNumber, ProviderPrice, ProviderStatus


class SupplierPoolProvider:
    """Adapter marker for DB-backed supplier inventory.

    The current MVP reserves supplier numbers through app.services.suppliers
    because selecting inventory, decrementing availability and creating a
    SupplierActivation must happen inside the same database transaction as the
    client Order. This class keeps the provider registry explicit so real
    supplier issuing can be moved behind an adapter without changing routing
    names.
    """

    def get_prices(self, service_code: str | None = None, country_iso2: str | None = None) -> list[ProviderPrice]:
        return []

    def get_number(self, service_code: str, country_iso2: str, operator: str | None = None) -> ProviderNumber:
        raise RuntimeError("Supplier pool reservations require database context")

    def get_order_status(self, provider_order_id: str) -> ProviderStatus:
        return ProviderStatus(status="waiting")

    def cancel_order(self, provider_order_id: str) -> bool:
        return True

    def finish_order(self, provider_order_id: str) -> bool:
        return True
