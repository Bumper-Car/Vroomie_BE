from sqlalchemy import Column, Integer, String, Float
from app.core.database import Base

class FeedbackLog(Base):
    __tablename__ = "feedback_log"
    id = Column(Integer, primary_key=True, index=True)
    run_number = Column(Integer, default=1)
    category = Column(String(50))
    timestamp = Column(Float)  # 발생 시각 (초 단위)
