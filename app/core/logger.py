import logging
import structlog

from logging.handlers import TimedRotatingFileHandler
from typing import Optional
from datetime import datetime


def setup_logging(log_file: Optional[str] = None) -> None:
    """Configure structured JSON logging using structlog with daily rotation."""

    logging.getLogger("pymongo").setLevel(logging.WARNING)
    logging.getLogger("motor").setLevel(logging.WARNING)

    structlog.configure(
        processors=[
            structlog.stdlib.filter_by_level,
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.UnicodeDecoder(),
            structlog.processors.JSONRenderer(),
        ],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )

    handlers = [
        logging.StreamHandler(),
    ]

    if log_file:
        # Use TimedRotatingFileHandler for daily rotation
        rotating_handler = TimedRotatingFileHandler(
            filename=log_file,
            when="midnight",
            interval=1,
            backupCount=30,
            utc=False,
        )
        rotating_handler.namer = lambda name: name.replace(".log", "") + datetime.now().strftime("%Y%m%d") + ".log"
        handlers.append(rotating_handler)

    # Configure standard logging first
    logging.basicConfig(
        format="%(message)s",
        level=logging.DEBUG,
        handlers=handlers,
        force=True,
    )

def get_logger(name: str) -> structlog.stdlib.BoundLogger:
    """Get a structlog logger instance."""
    return structlog.get_logger(name)
