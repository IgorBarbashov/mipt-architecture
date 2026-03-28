from __future__ import annotations

import json
import os
import time
from typing import Any, Dict, Optional

from .cache_interface import Cache


class FileCache(Cache):
    """Простейший файловый кэш на JSON с TTL для небольших данных"""

    def __init__(self, file_path: str) -> None:
        self._file_path = file_path

    def get(self, key: str) -> Optional[Any]:
        data = self._load_all()
        if not data:
            return None

        item = data.get(key)
        if not isinstance(item, dict):
            return None

        expires_at = item.get("expires_at")
        value = item.get("value")

        if expires_at is None or value is None:
            return None

        if time.time() > expires_at:
            return None

        return value

    def set(self, key: str, value: Any, ttl_seconds: int) -> None:
        data = self._load_all() or {}
        expires_at = time.time() + ttl_seconds

        data[key] = {
            "value": value,
            "expires_at": expires_at,
        }

        try:
            with open(self._file_path, "w", encoding="utf-8") as f:
                json.dump(data, f)
        except OSError:
            pass

    def _load_all(self) -> Optional[Dict[str, Any]]:
        if not os.path.exists(self._file_path):
            return None

        try:
            with open(self._file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except (OSError, json.JSONDecodeError):
            return None

        if not isinstance(data, dict):
            return None

        return data
