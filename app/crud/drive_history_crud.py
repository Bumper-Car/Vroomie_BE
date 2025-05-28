from sqlalchemy.orm import Session

from app.models.drive_history import DriveHistory
from app.models.user import User
from app.schemas.drive_history import DriveHistoriesResponse, DriveHistoriesItem


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
