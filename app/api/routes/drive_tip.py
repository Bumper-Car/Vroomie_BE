from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.dependencies import get_user
from app.core.database import get_db
from app.models import User
from app.schemas.drive_tip import DriveTipsResponse
from app.services import drive_tip_service

router = APIRouter(prefix="/drive/tips", tags=["drive_tip"])


@router.get(
    "",
    response_model=DriveTipsResponse,
    response_model_exclude_none=True,
)
def read_drive_tips(
        user: User = Depends(get_user),
        db: Session = Depends(get_db),
        fields: str = Query(None, description="응답할 필드 지정 (예: title)"),
):
    if fields == "title":
        return drive_tip_service.get_drive_tips_title(db)
    else:
        return drive_tip_service.get_drive_tips(db)