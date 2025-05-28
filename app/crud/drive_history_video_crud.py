from typing import List

from sqlalchemy.orm import Session

from app.models import DriveHistoryVideo
from app.schemas.drive_history import VideoItem

def get_videos_by_history_id(history_id: int, db: Session) -> List[DriveHistoryVideo]:
    return db.query(DriveHistoryVideo).filter(DriveHistoryVideo.history_id == history_id).all()

def create_video(history_id: int, videos_request: List[VideoItem], db: Session) -> List[DriveHistoryVideo]:
    drive_history_videos = []
    for v in videos_request:
        video = DriveHistoryVideo(
            history_id=history_id,
            title=v.title,
            content=v.content,
            video_url=v.url
        )
        db.add(video)
        drive_history_videos.append(video)
    return drive_history_videos
