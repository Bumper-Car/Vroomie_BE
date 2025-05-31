import enum
from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, Boolean, Enum
from sqlalchemy.orm import relationship

from app.core.database import Base


class DriveTip(Base):
    __tablename__ = "drive_tip"

    tip_id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255))
    thumbnail_url = Column(String(255))
    create_at = Column(DateTime, default=datetime.utcnow)
    content = Column(String(1000))
