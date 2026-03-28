from __future__ import annotations

API_URL_TEMPLATE = "https://api.exchangerate-api.com/v4/latest/{base}"
REQUEST_TIMEOUT_SECONDS = 10

CACHE_FILE_PATH = "exchange_rates_cache.json"
CACHE_TTL_SECONDS = 3600

MAX_RETRIES = 3
RETRY_DELAY_SECONDS = 2

BASE_CURRENCY = "USD"
TARGET_CURRENCIES = ["RUB", "EUR", "GBP", "CNY"]
