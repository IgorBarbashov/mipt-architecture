from __future__ import annotations

import config
from converters import (
    FileCache,
    HttpExchangeRateService,
    UniversalCurrencyConverter,
)
from logging_config import setup_logging


def read_amount() -> float:
    while True:
        raw = input("Введите значение в USD: ").strip()
        try:
            amount = float(raw.replace(",", "."))
            if amount < 0:
                print("Сумма не может быть отрицательной, попробуйте еще раз.")
                continue
            return amount
        except ValueError:
            print("Некорректное число, введите еще раз.")


def print_conversions(amount: float) -> None:
    cache = FileCache(config.CACHE_FILE_PATH)
    rate_service = HttpExchangeRateService(cache=cache)
    converter = UniversalCurrencyConverter(rate_service, base_currency="USD")

    for target in config.TARGET_CURRENCIES:
        try:
            result = converter.convert("USD", target, amount)
        except Exception as exc:
            print(f"Ошибка конвертации в {target}: {exc}")
            continue
        print(f"{amount} USD -> {result:.2f} {target}")


def main() -> None:
    setup_logging()
    amount = read_amount()
    print_conversions(amount)


if __name__ == "__main__":
    main()
