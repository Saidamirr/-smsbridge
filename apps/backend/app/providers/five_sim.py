from __future__ import annotations
from app.providers.base import ProviderNumber, ProviderPrice, ProviderStatus


class FiveSimProvider:
    # TODO: Add real 5sim-compatible integration when credentials and compliance review are ready.
    def get_prices(self, service_code: str | None = None, country_iso2: str | None = None) -> list[ProviderPrice]:
        return []

    def get_number(self, service_code: str, country_iso2: str, operator: str | None = None) -> ProviderNumber:
        raise NotImplementedError("FiveSimProvider is a placeholder")

    def get_order_status(self, provider_order_id: str) -> ProviderStatus:
        raise NotImplementedError("FiveSimProvider is a placeholder")

    def cancel_order(self, provider_order_id: str) -> bool:
        raise NotImplementedError("FiveSimProvider is a placeholder")

    def finish_order(self, provider_order_id: str) -> bool:
        raise NotImplementedError("FiveSimProvider is a placeholder")

