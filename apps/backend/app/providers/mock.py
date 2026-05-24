from __future__ import annotations
import random
import time
from decimal import Decimal
from uuid import uuid4

from app.core.config import settings
from app.providers.base import ProviderNumber, ProviderPrice, ProviderStatus

SERVICES = ["telegram", "whatsapp", "google", "facebook", "amazon", "openai"]
COUNTRIES = ["IN", "ID", "KZ", "UZ", "PH", "BR", "MX"]
COUNTRY_PREFIX = {"IN": "91", "ID": "62", "KZ": "7", "UZ": "998", "PH": "63", "BR": "55", "MX": "52"}


class MockProvider:
    def __init__(self, code: str = "mock"):
        self.code = code

    def get_prices(self, service_code: str | None = None, country_iso2: str | None = None) -> list[ProviderPrice]:
        rows: list[ProviderPrice] = []
        for service in SERVICES:
            for country in COUNTRIES:
                if service_code and service != service_code:
                    continue
                if country_iso2 and country != country_iso2:
                    continue
                base = Decimal("0.35") + Decimal(str((SERVICES.index(service) + COUNTRIES.index(country)) % 5)) / 10
                rows.append(
                    ProviderPrice(
                        service_code=service,
                        country_iso2=country,
                        operator=None,
                        provider_cost=base,
                        available_count=25,
                        delivery_rate=Decimal("88.50"),
                    )
                )
        return rows

    def get_number(self, service_code: str, country_iso2: str, operator: str | None = None) -> ProviderNumber:
        if "fail" in self.code:
            raise RuntimeError("Configured mock provider failure")
        ts = int(time.time())
        prefix = COUNTRY_PREFIX.get(country_iso2, "1")
        provider_order_id = f"{self.code}-{ts}-{uuid4().hex[:10]}"
        phone_number = f"+{prefix}{random.randint(100000000, 999999999)}"
        return ProviderNumber(provider_order_id=provider_order_id, phone_number=phone_number)

    def get_order_status(self, provider_order_id: str) -> ProviderStatus:
        try:
            created_ts = int(provider_order_id.split("-")[1])
        except (IndexError, ValueError):
            created_ts = int(time.time())
        age = int(time.time()) - created_ts
        if age < settings.mock_sms_delay_seconds:
            return ProviderStatus(status="waiting")
        if age > settings.mock_order_timeout_seconds:
            return ProviderStatus(status="timeout")
        deterministic = (sum(ord(ch) for ch in provider_order_id) % 100) / 100
        if deterministic <= settings.mock_success_rate:
            code = str(100000 + (sum(ord(ch) for ch in provider_order_id) % 899999))
            return ProviderStatus(status="sms_received", sms_code=code, sms_text=f"smsbridge test code: {code}")
        return ProviderStatus(status="waiting")

    def cancel_order(self, provider_order_id: str) -> bool:
        return True

    def finish_order(self, provider_order_id: str) -> bool:
        return True

