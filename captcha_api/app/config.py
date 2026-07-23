from dotenv import load_dotenv
import os

load_dotenv()

# ==========================
# APP
# ==========================

APP_NAME = os.getenv(
    "APP_NAME",
    "Captcha Gap Detection API"
)

# ==========================
# YOLO
# ==========================

MODEL_PATH = os.getenv(
    "MODEL_PATH",
    "best.pt"
)

YOLO_DEVICE = os.getenv(
    "YOLO_DEVICE",
    "cpu"
)

YOLO_IMAGE_SIZE = int(
    os.getenv("YOLO_IMAGE_SIZE", "640")
)

YOLO_CONFIDENCE = float(
    os.getenv("YOLO_CONFIDENCE", "0.25")
)

LOW_CONFIDENCE_THRESHOLD = float(
    os.getenv("LOW_CONFIDENCE_THRESHOLD", "0.5")
)

# ==========================
# MYSQL
# ==========================

MYSQL_HOST = os.getenv(
    "MYSQL_HOST",
    "127.0.0.1"
)

MYSQL_PORT = int(
    os.getenv("MYSQL_PORT", "3306")
)

MYSQL_DATABASE = os.getenv(
    "MYSQL_DATABASE",
    "captcha_ai"
)

MYSQL_USER = os.getenv(
    "MYSQL_USER",
    "root"
)

MYSQL_PASSWORD = os.getenv(
    "MYSQL_PASSWORD",
    ""
)