import logging
import sys


def setup_logger(name: str = "cti_nexus", level: int = logging.INFO) -> logging.Logger:
    """Configures and returns a structured logger."""
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(level)
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(level)
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    return logger


logger = setup_logger()
