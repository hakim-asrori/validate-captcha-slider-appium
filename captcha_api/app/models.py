from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    Boolean,
    DateTime
)

from sqlalchemy.sql import func

from app.database import Base


class DetectionLog(Base):
    __tablename__ = "detection_logs"

    id = Column(Integer, primary_key=True, index=True)

    request_id = Column(String(20), unique=True, nullable=False, index=True)

    filename = Column(String(255), nullable=False)

    file_size = Column(Integer)

    detected = Column(Boolean, nullable=False)

    status = Column(String(30), nullable=False)

    confidence = Column(Float)

    bbox_x1 = Column(Float)
    bbox_y1 = Column(Float)
    bbox_x2 = Column(Float)
    bbox_y2 = Column(Float)

    gap_center_x = Column(Float)
    gap_center_y = Column(Float)

    screenshot_path = Column(String(500))

    read_time = Column(Float)
    decode_time = Column(Float)
    predict_time = Column(Float)
    process_time = Column(Float)
    total_time = Column(Float)

    message = Column(String(255))

    created_at = Column(
        DateTime,
        server_default=func.now(),
        nullable=False
    )