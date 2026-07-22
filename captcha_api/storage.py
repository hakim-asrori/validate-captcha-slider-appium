from pathlib import Path
from datetime import datetime
import cv2

BASE_DIR = Path("storage/screenshots")

FAILED_DIR = BASE_DIR / "failed"
LOW_CONF_DIR = BASE_DIR / "low-confidence"
EXCEPTION_DIR = BASE_DIR / "exception"

FAILED_DIR.mkdir(parents=True, exist_ok=True)
LOW_CONF_DIR.mkdir(parents=True, exist_ok=True)
EXCEPTION_DIR.mkdir(parents=True, exist_ok=True)


def _generate_filename(prefix: str):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    return f"{prefix}_{timestamp}.png"


def save_failed(image):
    filename = FAILED_DIR / _generate_filename("failed")
    cv2.imwrite(str(filename), image)
    return str(filename)


def save_low_confidence(image):
    filename = LOW_CONF_DIR / _generate_filename("low_conf")
    cv2.imwrite(str(filename), image)
    return str(filename)


def save_exception(image):
    filename = EXCEPTION_DIR / _generate_filename("exception")
    cv2.imwrite(str(filename), image)
    return str(filename)