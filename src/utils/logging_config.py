import logging
import os
import re
import sys
from logging.handlers import RotatingFileHandler

# Recommended log format
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

# Sensitive data patterns (simple example)
SENSITIVE_PATTERNS = {
    # Add regex patterns for sensitive data you want to mask.
    # e.g., 'ssn': r'\d{3}-\d{2}-\d{4}'
}


def sanitize_for_logging(data: object) -> str:
    """
    Sanitizes a given data object by converting it to a string and masking
    any substrings that match predefined sensitive patterns.

    This is a simple implementation. For production systems, consider more
    robust and context-aware sanitization libraries or techniques.

    Args:
        data: The data to be sanitized (can be any object).

    Returns:
        A sanitized string representation of the data.
    """
    s = str(data)
    for _key, pattern in SENSITIVE_PATTERNS.items():
        s = re.sub(pattern, "[REDACTED]", s)
    return s


def get_logger(
    name: str,
    log_level: str = None,
    log_to_file: bool = False,
    log_directory: str = "logs",
):
    """
    Configures and returns a logger instance.

    Args:
        name (str): The name for the logger, typically __name__.
        log_level (str, optional): The logging level. If not provided, it
            defaults to DEBUG if DEBUG_MODE=true, otherwise INFO.
        log_to_file (bool): If True, logs will also be written to a file.
        log_directory (str): The directory to save log files in.

    Returns:
        logging.Logger: A configured logger instance.
    """
    # Determine log level from environment or argument
    if log_level is None:
        debug_mode = os.environ.get("DEBUG_MODE", "false").lower() == "true"
        level = logging.DEBUG if debug_mode else logging.INFO
    else:
        level = logging.getLevelName(log_level.upper())

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.propagate = False  # Avoid duplicate logs in parent loggers

    # Clear existing handlers to prevent duplicate messages
    if logger.hasHandlers():
        logger.handlers.clear()

    # Console Handler
    console_handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(LOG_FORMAT, datefmt=LOG_DATE_FORMAT)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # File Handler (optional)
    if log_to_file:
        os.makedirs(log_directory, exist_ok=True)
        log_file = os.path.join(log_directory, f"{name.replace('.', '_')}.log")
        # Rotating file handler to keep log files from growing too large
        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=10 * 1024 * 1024,
            backupCount=5,  # 10 MB
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger


# Example of a default logger that can be used for quick debugging
# You can import this directly or use get_logger for more control.
default_logger = get_logger("default")
