from sqlalchemy.orm import Session

from app.crud import drive_history_crud, drive_history_video_crud
from app.models.user import User
from app.schemas.drive_history import DriveHistoryRequest, DriveHistoryResponse, VideoItem


def get_drive_histories(db: Session, user: User):
    return drive_history_crud.get_histories(db, user)


def get_drive_history(history_id: int, db: Session, user: User):
    drive_history = drive_history_crud.get_history(history_id, db, user.user_id)
    drive_history_videos = drive_history_video_crud.get_videos_by_history_id(history_id, db)

    return DriveHistoryResponse(
        start_at=drive_history.start_at,
        end_at=drive_history.end_at,
        start_location=drive_history.start_location,
        end_location=drive_history.end_location,
        distance=drive_history.distance,
        duration=drive_history.duration,
        score=drive_history.score,
        lane_deviation_left_count=drive_history.lane_deviation_left_count,
        lane_deviation_right_count=drive_history.lane_deviation_right_count,
        safe_distance_violation_count=drive_history.safe_distance_violation_count,
        sudden_deceleration_count=drive_history.sudden_deceleration_count,
        sudden_acceleration_count=drive_history.sudden_acceleration_count,
        speeding_count=drive_history.speeding_count,
        videos=[
            VideoItem(
                video_id=video.history_video_id,
                title=video.title,
                content=video.content,
                url=video.video_url
            ) for video in drive_history_videos
        ]
    )

def create_drive_history(drive_history_request: DriveHistoryRequest, db: Session, user: User):
    drive_history = drive_history_crud.create_history(drive_history_request, db, user.user_id)
    db.flush()
    drive_history_videos = drive_history_video_crud.create_video(drive_history.history_id, drive_history_request.videos, db)
    db.commit()
    db.refresh(drive_history)
    return DriveHistoryResponse(
        start_at=drive_history.start_at,
        end_at=drive_history.end_at,
        start_location=drive_history.start_location,
        end_location=drive_history.end_location,
        distance=drive_history.distance,
        duration=drive_history.duration,
        score=drive_history.score,
        lane_deviation_left_count=drive_history.lane_deviation_left_count,
        lane_deviation_right_count=drive_history.lane_deviation_right_count,
        safe_distance_violation_count=drive_history.safe_distance_violation_count,
        sudden_deceleration_count=drive_history.sudden_deceleration_count,
        sudden_acceleration_count=drive_history.sudden_acceleration_count,
        speeding_count=drive_history.speeding_count,
        videos=[
            VideoItem(
                video_id=v.history_video_id,
                title=v.title,
                content=v.content,
                url=v.video_url
            )
            for v in drive_history_videos
        ]
    )