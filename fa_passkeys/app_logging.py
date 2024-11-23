# logging.py

import logging
from fa_passkeys.config import settings

logger = logging.getLogger("fa_passkeys")


def setup_logging():
    level = getattr(logging, settings.logging_level.upper(), logging.INFO)
    logger.setLevel(level)

    # Clear existing handlers
    logger.handlers = []

    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

    if "console" in settings.logging_handlers:
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    if "file" in settings.logging_handlers:
        file_handler = logging.FileHandler(settings.logging_file_path)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)


# Initialize logging
setup_logging()
