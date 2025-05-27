from sqlalchemy import Column, String, ForeignKey, DateTime, Float, Integer, func

from app.core.database import Base

class DriveStatistic(Base):
    __tablename__ = "drive_statistic"

    drive_statistic = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.user_id"), nullable=False)

    year = Column(Integer)
    month = Column(Integer)

    distance = Column(Float)  # km 단위
    duration = Column(Integer)  # 분 단위

    lane_deviation_count = Column(Integer)
    safe_distance_violation_count = Column(Integer)
    sudden_deceleration_count = Column(Integer)
    sudden_acceleration_count = Column(Integer)
    speeding_count = Column(Integer)

    monthly_score = Column(Integer)