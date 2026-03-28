import logging
from typing import Optional


def setup_logging() -> None:
    """Глобальная настройка логирования"""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )


def get_logger(name: Optional[str] = None) -> logging.Logger:
    """Единая фабрика логгеров для всего приложения"""
    return logging.getLogger(name or __name__)
