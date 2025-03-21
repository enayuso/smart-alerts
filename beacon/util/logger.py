import sys
from typing import Literal

from loguru import logger

_LEVELS = Literal["TRACE", "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
_LOG_LEVEL: _LEVELS = "INFO"


def set_log_level(level: _LEVELS):
    global _LOG_LEVEL
    _LOG_LEVEL = level

async def configure_warnings():
    import warnings
    warnings.filterwarnings("ignore", message=r"\[W008\]", category=UserWarning)

logger.remove()
logger.add(sys.stderr, filter=lambda r: r["level"].no >= logger.level(_LOG_LEVEL).no)
