import logging
from rich.logging import RichHandler

LOGGER_NAME = "devc"

def setup_logging(level=logging.INFO):
    if not logging.getLogger().handlers:  # only configure once
        logging.basicConfig(
            level="NOTSET",
            format="%(message)s",
            datefmt="[%X]",
            handlers=[RichHandler(rich_tracebacks=True, markup=True)],
        )
    root = logging.getLogger(LOGGER_NAME)
    root.setLevel(level)
    return root

def get_logger(name=None):
    return logging.getLogger(f"{LOGGER_NAME}.{name}" if name else LOGGER_NAME)