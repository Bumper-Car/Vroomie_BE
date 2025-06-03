from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencies import get_user
from app.core.database import get_db
from app.models.user import User
from app.schemas.drive_history import DriveHistoriesResponse, DriveHistoryResponse, DriveHistoryRequest
from app.services import drive_history_service

router = APIRouter(prefix="/drive/histories", tags=["drive_history"])

@router.get(
    "",
    response_model=DriveHistoriesResponse,
)
def read_histories(
        user: User = Depends(get_user),
        db: Session = Depends(get_db)
):
    return drive_history_service.get_drive_histories(db, user)


@router.get(
    "/{history_id}",
    response_model=DriveHistoryResponse,
)
def read_history(
        history_id: int,
        user: User = Depends(get_user),
        db: Session = Depends(get_db)
):
    return drive_history_service.get_drive_history(history_id, db, user)

@router.post(
    "",
    response_model=DriveHistoryResponse,
)
def create_history(
        drive_history_request: DriveHistoryRequest,
        user: User = Depends(get_user),
        db: Session = Depends(get_db)
):
    return drive_history_service.create_drive_history(drive_history_request, db, user)

@router.post(
    "/devtest",
    response_model=DriveHistoryResponse,
)
def create_history_devtest(
        drive_history_request: DriveHistoryRequest,
        db: Session = Depends(get_db)
):
    # ⚠️ 테스트용: 로그인 없이 user_id=3 고정
    from app.models.user import User
    user = User(user_id=3)

    return drive_history_service.create_drive_history(drive_history_request, db, user)
