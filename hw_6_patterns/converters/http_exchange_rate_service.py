from __future__ import annotations

import json
import logging
import time
from typing import Dict, Optional

import requests

import config
from logging_config import get_logger

from .cache_interface import Cache
from .exchange_rate_service_interface import ExchangeRateService


class HttpExchangeRateService(ExchangeRateService):
    """HTTP‑сервис курсов: API + ретраи + кэш + логирование через DI"""

    def __init__(
        self,
        cache: Cache,
        api_url_template: str = config.API_URL_TEMPLATE,
        cache_ttl_seconds: int = config.CACHE_TTL_SECONDS,
        max_retries: int = config.MAX_RETRIES,
        retry_delay_seconds: int = config.RETRY_DELAY_SECONDS,
        request_timeout: int = config.REQUEST_TIMEOUT_SECONDS,
        logger: Optional[logging.Logger] = None,
    ) -> None:
        self._cache = cache
        self._api_url_template = api_url_template
        self._cache_ttl_seconds = cache_ttl_seconds
        self._max_retries = max_retries
        self._retry_delay_seconds = retry_delay_seconds
        self._request_timeout = request_timeout
        self._logger = logger or get_logger(__name__)

    def get_rates(self, base_currency: str) -> Dict[str, float]:
        base_currency = base_currency.upper()
        cache_key = self._cache_key(base_currency)

        cached = self._cache.get(cache_key)
        if isinstance(cached, dict):
            self._logger.info("Using cached rates for base=%s", base_currency)
            return cached

        self._logger.info("Cache miss for base=%s, fetching from API", base_currency)
        rates = self._fetch_with_retries(base_currency)
        self._cache.set(cache_key, rates, self._cache_ttl_seconds)
        return rates

    def _cache_key(self, base_currency: str) -> str:
        return f"rates:{base_currency}"

    def _fetch_with_retries(self, base_currency: str) -> Dict[str, float]:
        url = self._api_url_template.format(base=base_currency)
        last_exception: Optional[Exception] = None

        for attempt in range(1, self._max_retries + 1):
            try:
                response = requests.get(url, timeout=self._request_timeout)
                response.raise_for_status()
                data = response.json()
                rates = data.get("rates")
                if not isinstance(rates, dict):
                    raise ValueError("Invalid 'rates' format in API response")
                return rates
            except (requests.RequestException, ValueError, json.JSONDecodeError) as exc:
                last_exception = exc
                self._logger.error(
                    "Request failed (attempt %s/%s): %s",
                    attempt,
                    self._max_retries,
                    exc,
                )
                if attempt < self._max_retries:
                    time.sleep(self._retry_delay_seconds)

        assert last_exception is not None
        raise RuntimeError("Unable to fetch exchange rates") from last_exception
