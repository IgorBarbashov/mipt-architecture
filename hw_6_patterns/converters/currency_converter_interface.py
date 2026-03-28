from __future__ import annotations

from abc import ABC, abstractmethod


class CurrencyConverter(ABC):
    """Абстрактный конвертер валют"""

    @abstractmethod
    def convert(self, from_currency: str, to_currency: str, amount: float) -> float:
        """Конвертировать amount из from_currency в to_currency"""
        raise NotImplementedError
