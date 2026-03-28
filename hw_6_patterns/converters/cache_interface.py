from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Optional


class Cache(ABC):
    """Абстракция кэша с простым API"""

    @abstractmethod
    def get(self, key: str) -> Optional[Any]:
        """Получить значение по ключу или None, если нет или истек TTL"""
        raise NotImplementedError

    @abstractmethod
    def set(self, key: str, value: Any, ttl_seconds: int) -> None:
        """Сохранить значение с ограничением по времени жизни"""
        raise NotImplementedError
