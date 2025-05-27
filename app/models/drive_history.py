from sqlalchemy import Column, String, ForeignKey, DateTime, Float, Integer, func
from sqlalchemy.orm import relationship

from app.core.database import Base

class DriveHistory(Base):
    __tablename__ = "drive_history"

    history_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.user_id"), nullable=False)

    start_at = Column(DateTime(timezone=True))
    end_at = Column(DateTime(timezone=True))

    start_location = Column(String(100))
    end_location = Column(String(100))

    distance = Column(Float)  # km 단위
    duration = Column(Integer)  # 분 단위

    score = Column(Integer)

    lane_deviation_left_count = Column(Integer)
    lane_deviation_right_count = Column(Integer)
    safe_distance_violation_count = Column(Integer)
    sudden_deceleration_count = Column(Integer)
    sudden_acceleration_count = Column(Integer)
    speeding_count = Column(Integer)

    videos = relationship("DriveHistoryVideo", backref="drive_history")