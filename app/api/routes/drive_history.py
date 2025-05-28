from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencies import get_user
from app.core.database import get_db
from app.models.user import User
from app.schemas.drive_history import DriveHistoriesResponse
from app.services import drive_history_service

router = APIRouter(prefix="/drive/histories", tags=["drive_history"])

@router.get(
    "",
    response_model=DriveHistoriesResponse,
)
def read_user_score(
        user: User = Depends(get_user),
        db: Session = Depends(get_db)
):
    return drive_history_service.get_drive_histories(db, user)