from sqlalchemy.orm import Session

from app.models.drive_history import DriveHistory
from app.models.user import User
from app.schemas.drive_history import DriveHistoriesResponse, DriveHistoriesItem, DriveHistoryResponse, VideoItem, \
    DriveHistoryRequest
from app.services.drive_score_service import calculate_drive_score
from typing import Optional


def get_histories(db: Session, user: User) -> list[DriveHistory]:
    histories = (
        db.query(DriveHistory)
        .filter(DriveHistory.user_id == user.user_id)
        .order_by(DriveHistory.start_at.desc())
        .all()
    )

    return histories


def get_history(history_id, db: Session, user_id: int) -> DriveHistory:
    history_query = (((db.query(DriveHistory)
                     .filter(DriveHistory.history_id == history_id))
                     .filter(DriveHistory.user_id == user_id))
                     .first())

    return DriveHistory(
        history_id=history_id,
        user_id=user_id,
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
    )

def create_history(drive_history_request: DriveHistoryRequest, db: Session, user_id: int) -> DriveHistory:
    drive_history = DriveHistory(
        user_id=user_id,
        start_at=drive_history_request.start_at,
        end_at=drive_history_request.end_at,
        start_location=drive_history_request.start_location,
        end_location=drive_history_request.end_location,
        distance=drive_history_request.distance,
        duration=drive_history_request.duration,
        lane_deviation_left_count=drive_history_request.lane_deviation_left_count,
        lane_deviation_right_count=drive_history_request.lane_deviation_right_count,
        safe_distance_violation_count=drive_history_request.safe_distance_violation_count,
        sudden_deceleration_count=drive_history_request.sudden_deceleration_count,
        sudden_acceleration_count=drive_history_request.sudden_acceleration_count,
        speeding_count=drive_history_request.speeding_count,
    )
    db.add(drive_history)
    return drive_history

def get_all_histories_score(db: Session):
    return (db.query(DriveHistory)
            .filter(DriveHistory.score.isnot(None))
            .all())


def get_all_drive_scores(db: Session):
    return db.query(DriveHistory.score).filter(DriveHistory.score.isnot(None)).all()

def get_latest_history_by_user_id(db: Session, user_id: int) -> Optional[DriveHistory]:
    return (
        db.query(DriveHistory)
        .filter(DriveHistory.user_id == user_id)
        .order_by(DriveHistory.start_at.desc())
        .first()
    )


def get_my_recent_histories_score(db: Session, user_id: int):
    return (db.query(DriveHistory)
            .filter(DriveHistory.user_id == user_id)
            .filter(DriveHistory.score.isnot(None))
            .order_by(DriveHistory.start_at.desc())
            .limit(10)
            .all())

