from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models import DetectionLog


class DetectionRepository:

    @staticmethod
    def save(data: dict):

        db: Session = SessionLocal()

        try:

            log = DetectionLog(

                request_id=data["request_id"],

                filename=data["filename"],

                file_size=data["file_size"],

                detected=data["detected"],

                status=data["status"],

                confidence=data.get("confidence"),

                gap_center_x=(data.get("gap_center") or {}).get("x"),

                gap_center_y=(data.get("gap_center") or {}).get("y"),

                bbox_x1=(data.get("bbox") or {}).get("x1"),

                bbox_y1=(data.get("bbox") or {}).get("y1"),

                bbox_x2=(data.get("bbox") or {}).get("x2"),

                bbox_y2=(data.get("bbox") or {}).get("y2"),

                screenshot_path=data.get("screenshot_path"),

                read_time=data["timing"]["read"],

                decode_time=data["timing"]["decode"],

                predict_time=data["timing"]["predict"],

                process_time=data["timing"]["process"],

                total_time=data["timing"]["total"],

                message=data.get("message"),

            )

            db.add(log)

            db.commit()

            db.refresh(log)

            return log

        except Exception:

            db.rollback()

            raise

        finally:

            db.close()
