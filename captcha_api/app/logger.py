import logging
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path

# Buat folder logs jika belum ada
Path("logs").mkdir(exist_ok=True)

logger = logging.getLogger("captcha-service")
logger.setLevel(logging.INFO)

# Hindari duplicate log
if not logger.handlers:
    logger.propagate = False

handler = TimedRotatingFileHandler(
    filename="logs/app.log",
    when="midnight",
    interval=1,
    backupCount=30,
    encoding="utf-8"
)

handler.suffix = "%Y-%m-%d"

formatter = logging.Formatter(
    "%(asctime)s | %(levelname)s | %(message)s"
)

handler.setFormatter(formatter)

logger.addHandler(handler)