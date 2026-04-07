"""
General helper functions.
"""
import logging
import os

def setup_logger(name="drug_interaction", level=logging.INFO):
    """Configure and return a standard logger."""
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            "%(asctime)s | %(name)s | %(levelname)s | %(message)s"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    logger.setLevel(level)
    return logger

def get_env(key, default=None):
    """Read an environment variable with a fallback."""
    return os.getenv(key, default)
