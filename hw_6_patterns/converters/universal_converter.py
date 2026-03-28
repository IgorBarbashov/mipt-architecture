from __future__ import annotations

from typing import Dict

import config

from .currency_converter_interface import CurrencyConverter
from .exchange_rate_service_interface import ExchangeRateService


class UniversalCurrencyConverter(CurrencyConverter):
    """Универсальный конвертер на базе сервиса курсов"""

    def __init__(
        self,
        rate_service: ExchangeRateService,
        base_currency: str = config.BASE_CURRENCY,
    ) -> None:
        self._rate_service = rate_service
        self._base_currency = base_currency.upper()
        self._rates: Dict[str, float] = self._rate_service.get_rates(
            self._base_currency
        )

    def convert(self, from_currency: str, to_currency: str, amount: float) -> float:
        from_currency = from_currency.upper()
        to_currency = to_currency.upper()

        if from_currency == to_currency:
            return amount

        if from_currency != self._base_currency:
            raise ValueError(
                f"Converter supports only base currency {self._base_currency}, "
                f"got from_currency={from_currency}"
            )

        try:
            rate = self._rates[to_currency]
        except KeyError as exc:
            raise ValueError(f"Unsupported target currency: {to_currency}") from exc

        return amount * rate

    def supported_currencies(self) -> Dict[str, float]:
        """Вернуть словарь поддерживаемых валют и их курсов относительно базы"""
        return dict(self._rates)
