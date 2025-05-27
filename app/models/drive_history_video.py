from sqlalchemy import Column, String, ForeignKey, Integer

from app.core.database import Base

class DriveHistoryVideo(Base):
    __tablename__ = "drive_history_video"

    history_video_id = Column(Integer, primary_key=True, index=True)
    history_id = Column(Integer, ForeignKey("drive_history.history_id"), nullable=False)

    title = Column(String(255))
    content = Column(String(1000))
    video_url = Column(String(1000))
