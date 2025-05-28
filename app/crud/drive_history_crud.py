from sqlalchemy.orm import Session

from app.models.drive_history import DriveHistory
from app.models.user import User
from app.schemas.drive_history import DriveHistoriesResponse, DriveHistoriesItem, DriveHistoryResponse, VideoItem


def get_histories(db: Session, user: User) -> DriveHistoriesResponse:
    histories_query = (
        db.query(DriveHistory)
        .filter(DriveHistory.user_id == user.user_id)
        .order_by(DriveHistory.start_at.desc())
        .all()
    )

    histories = [
        DriveHistoriesItem(
            history_id=h.history_id,
            start_at=h.start_at,
            end_at=h.end_at,
            start_location=h.start_location,
            end_location=h.end_location,
            score=h.score
        )
        for h in histories_query
    ]

    return DriveHistoriesResponse(histories=histories)


def get_history(history_id, db: Session, user: User) -> DriveHistoryResponse:
    history_query = (((db.query(DriveHistory)
                     .filter(DriveHistory.history_id == history_id))
                     .filter(DriveHistory.user_id == user.user_id))
                     .first())

    video_items = [
        VideoItem(
            video_id=str(video.video_id),
            title=video.title,
            content=video.content,
            url=video.url
        )
        for video in history_query.videos
    ]

    return DriveHistoryResponse(
        start_at=history_query.start_at,
        end_at=history_query.end_at,
        start_location=history_query.start_location,
        end_location=history_query.end_location,
        distance=history_query.distance,
        duration=history_query.duration,
        score=history_query.score,
        lane_deviation_left_count=history_query.lane_deviation_left_count,
        lane_deviation_right_count=history_query.lane_deviation_right_count,
        safe_distance_violation_count=history_query.safe_distance_violation_count,
        sudden_deceleration_count=history_query.sudden_deceleration_count,
        sudden_acceleration_count=history_query.sudden_acceleration_count,
        speeding_count=history_query.speeding_count,
        videos=video_items
    )