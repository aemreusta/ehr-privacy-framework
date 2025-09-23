"""
Centralized debugging and logging utility.

This module provides pre-configured logger instances for different parts of the
application, following the security and logging best practices.

- `debug`: A logger for client-side or general-purpose logging.
- `debug_server`: A logger for server-side or backend processes.
- `sanitize_for_logging`: A function to clean sensitive data before logging.

The log level is controlled by the `DEBUG_MODE` environment variable.
Set `DEBUG_MODE=true` for detailed `DEBUG` level output.
Defaults to `INFO` level for production.
"""

from .logging_config import get_logger, sanitize_for_logging

# Logger for general or client-facing operations (e.g., Streamlit)
debug = get_logger("app")

# Logger for backend or server-side operations (e.g., data processing)
debug_server = get_logger("server")

# You can also create more specific loggers as needed
# e.g., db_logger = get_logger("database", log_to_file=True)

__all__ = ["debug", "debug_server", "sanitize_for_logging"]
