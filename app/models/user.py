import enum
from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, Boolean, Enum
from sqlalchemy.orm import relationship

from app.core.database import Base

# 차량 종류 Enum
class CarTypeEnum(enum.Enum):
    COMPACT = "경차"
    PASSENGER = "승용차"
    SMALL_TRUCK = "소형화물차"
    MEDIUM = "중형차"
    LARGE = "대형차"
    HEAVY_TRUCK = "대형화물차"
    SPECIAL_TRUCK = "특수화물차"

# 연료 종류 Enum
class FuelTypeEnum(enum.Enum):
    GASOLINE = "휘발유"
    DIESEL = "경유"
    ELECTRIC = "전기"
    LPG = "LPG"
    PREMIUM_GASOLINE = "고급휘발유"

class User(Base):
    __tablename__ = "user"

    user_id = Column(Integer, primary_key=True, index=True)
    kakao_id = Column(String(20), nullable=False, unique=True)
    user_name = Column(String(100))
    create_at = Column(DateTime, default=datetime.utcnow)
    car_model = Column(String(100))
    car_hipass = Column(Boolean)
    car_type = Column(Enum(CarTypeEnum))
    car_fuel = Column(Enum(FuelTypeEnum))
    user_score = Column(Integer, default=0)
    drive_histories = relationship("DriveHistory", backref="user")
    drive_statistics = relationship("DriveStatistic", backref="user")