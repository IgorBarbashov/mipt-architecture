from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Dict


class ExchangeRateService(ABC):
    """Абстракция источника курсов валют"""

    @abstractmethod
    def get_rates(self, base_currency: str) -> Dict[str, float]:
        """Вернуть словарь курсов относительно base_currency"""
        raise NotImplementedError
