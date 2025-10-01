import logging
from rich.logging import RichHandler


def setup_logging() -> logging.Logger:
    FORMAT = "%(message)s"
    logging.basicConfig(
        level="NOTSET", format=FORMAT, datefmt="[%X]", handlers=[RichHandler(rich_tracebacks=True)]
    )

    logger = logging.getLogger("rtwcli")
    logger.setLevel(logging.DEBUG)  # global log level

    return logger


# Create and export the logger
logger = setup_logging()