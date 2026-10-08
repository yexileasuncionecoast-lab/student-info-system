"""Logging setup: writes to both console and a log file."""
import logging
from pathlib import Path


def setup_logger(log_file: str, level: str = "INFO") -> logging.Logger:
    """Create (or reuse) the application logger."""
    logger = logging.getLogger("sis")
    if logger.handlers:  # already configured
        return logger

    logger.setLevel(getattr(logging, level.upper(), logging.INFO))
    fmt = logging.Formatter("%(asctime)s | %(levelname)-8s | %(name)s | %(message)s")

    Path(log_file).parent.mkdir(parents=True, exist_ok=True)
    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setFormatter(fmt)
    logger.addHandler(file_handler)

    console = logging.StreamHandler()
    console.setLevel(logging.WARNING)  # keep the CLI menu clean
    console.setFormatter(fmt)
    logger.addHandler(console)
    return logger
