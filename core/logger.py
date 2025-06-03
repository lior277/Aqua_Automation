import logging
from typing import Dict

_LOGGER_CONFIG: Dict[str, logging.Logger] = {}


def get_logger(name: str) -> logging.Logger:
    if name in _LOGGER_CONFIG:
        return _LOGGER_CONFIG[name]

    logger = logging.getLogger(name)
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

    _LOGGER_CONFIG[name] = logger
    return logger
