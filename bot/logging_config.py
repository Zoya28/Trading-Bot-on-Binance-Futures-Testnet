import logging
import os

def setup_logger(name: str = "trading_bot") -> logging.Logger:
    """Set up a logger that writes to both console and a log file."""
    
    os.makedirs("logs", exist_ok=True)
    
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # Avoid adding duplicate handlers if called multiple times
    if logger.handlers:
        return logger

    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # File handler — logs everything (DEBUG and above)
    file_handler = logging.FileHandler("logs/trading_bot.log")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    # Console handler — only INFO and above (keeps terminal clean)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger