from __future__ import annotations
from dataclasses import dataclass
from decimal import Decimal
from typing import Protocol


@dataclass(frozen=True)
class ProviderPrice:
    service_code: str
    country_iso2: str
    operator: str | None
    provider_cost: Decimal
    available_count: int
    delivery_rate: Decimal


@dataclass(frozen=True)
class ProviderNumber:
    provider_order_id: str
    phone_number: str


@dataclass(frozen=True)
class ProviderStatus:
    status: str
    sms_code: str | None = None
    sms_text: str | None = None


class BaseProvider(Protocol):
    def get_prices(self, service_code: str | None = None, country_iso2: str | None = None) -> list[ProviderPrice]:
        ...

    def get_number(self, service_code: str, country_iso2: str, operator: str | None = None) -> ProviderNumber:
        ...

    def get_order_status(self, provider_order_id: str) -> ProviderStatus:
        ...

    def cancel_order(self, provider_order_id: str) -> bool:
        ...

    def finish_order(self, provider_order_id: str) -> bool:
        ...

