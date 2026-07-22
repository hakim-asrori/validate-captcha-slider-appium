from fastapi import UploadFile, HTTPException
from ultralytics import YOLO

import cv2
import numpy as np
import time
from uuid import uuid4

from logger import logger
from storage import (
    save_failed,
    save_low_confidence,
    save_exception
)

from config import LOW_CONFIDENCE_THRESHOLD

logger.info("Loading YOLO model...")
model = YOLO("best.pt")
logger.info("YOLO model loaded successfully.")


async def detect_gap(file: UploadFile):

    request_id = str(uuid4())[:8]

    start = time.perf_counter()

    img = None

    logger.info(
        f"[{request_id}] REQUEST | filename={file.filename} | type={file.content_type}"
    )

    try:

        # =====================================
        # Validate
        # =====================================

        if (
            file.content_type is None
            or not file.content_type.startswith("image/")
        ):
            logger.warning(
                f"[{request_id}] Invalid file type"
            )

            raise HTTPException(
                status_code=400,
                detail="File harus berupa gambar"
            )

        # =====================================
        # Read
        # =====================================

        contents = await file.read()

        read_time = time.perf_counter()

        logger.info(
            f"[{request_id}] REQUEST | size={len(contents)} bytes"
        )

        # =====================================
        # Decode
        # =====================================

        nparr = np.frombuffer(contents, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        decode_time = time.perf_counter()

        if img is None:

            logger.warning(
                f"[{request_id}] Image corrupt"
            )

            raise HTTPException(
                status_code=400,
                detail="Gagal membaca gambar"
            )

        # =====================================
        # Inference
        # =====================================

        results = model.predict(
            source=img,
            imgsz=640,
            conf=0.1,
            device="cpu",
            verbose=False
        )

        predict_time = time.perf_counter()

        result = results[0]

        # =====================================
        # No Detection
        # =====================================

        if len(result.boxes) == 0:

            screenshot = save_failed(img)

            end = time.perf_counter()

            logger.warning(
                f"[{request_id}] RESPONSE "
                f"| detected=False "
                f"| screenshot={screenshot}"
            )

            logger.info(
                f"[{request_id}] TIMING "
                f"| read={(read_time-start)*1000:.2f}ms "
                f"| decode={(decode_time-read_time)*1000:.2f}ms "
                f"| predict={(predict_time-decode_time)*1000:.2f}ms "
                f"| process={(end-predict_time)*1000:.2f}ms "
                f"| total={(end-start)*1000:.2f}ms"
            )

            return {
                "detected": False,
                "message": "Tidak ada gap terdeteksi"
            }

        # =====================================
        # Best Detection
        # =====================================

        best_idx = result.boxes.conf.argmax().item()
        box = result.boxes[best_idx]

        x1, y1, x2, y2 = box.xyxy[0].tolist()

        conf = float(box.conf[0].item())

        gap_center_x = (x1 + x2) / 2
        gap_center_y = (y1 + y2) / 2

        # =====================================
        # Low Confidence
        # =====================================

        if conf < LOW_CONFIDENCE_THRESHOLD:

            annotated = result.plot()

            screenshot = save_low_confidence(
                annotated
            )

            logger.warning(
                f"[{request_id}] LOW_CONFIDENCE "
                f"| confidence={conf:.4f} "
                f"| screenshot={screenshot}"
            )

        end = time.perf_counter()

        logger.info(
            f"[{request_id}] RESPONSE "
            f"| detected=True "
            f"| confidence={conf:.4f} "
            f"| center=({gap_center_x:.2f},{gap_center_y:.2f})"
        )

        logger.info(
            f"[{request_id}] TIMING "
            f"| read={(read_time-start)*1000:.2f}ms "
            f"| decode={(decode_time-read_time)*1000:.2f}ms "
            f"| predict={(predict_time-decode_time)*1000:.2f}ms "
            f"| process={(end-predict_time)*1000:.2f}ms "
            f"| total={(end-start)*1000:.2f}ms"
        )

        return {
            "detected": True,
            "confidence": round(conf, 4),
            "bbox": {
                "x1": round(x1, 2),
                "y1": round(y1, 2),
                "x2": round(x2, 2),
                "y2": round(y2, 2)
            },
            "gap_center": {
                "x": round(gap_center_x, 2),
                "y": round(gap_center_y, 2)
            }
        }

    except HTTPException:
        raise

    except Exception:

        try:

            if img is not None:

                screenshot = save_exception(img)

                logger.exception(
                    f"[{request_id}] Unexpected error "
                    f"| screenshot={screenshot}"
                )

            else:

                logger.exception(
                    f"[{request_id}] Unexpected error before image loaded"
                )

        except Exception:

            logger.exception(
                f"[{request_id}] Failed to save exception screenshot"
            )

        raise HTTPException(
            status_code=500,
            detail="Internal Server Error"
        )