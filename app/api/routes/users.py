from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.api.dependencies import get_user
from app.core.database import get_db
from app.models.user import User
from app.schemas.user import UserScoreResponse, UserExtraInfoRequest
from app.services import user_service

router = APIRouter(prefix="/users", tags=["users"])

@router.get(
    "/drive/score",
    response_model=UserScoreResponse,
)
def read_user_score(
        user: User = Depends(get_user)
):
    return user_service.get_user_score(user)

@router.post(
    ""
)


@router.post(
    "/extra",
)
def create_user_extra_info(
        user_request: UserExtraInfoRequest,
        user: User = Depends(get_user),
        db: Session = Depends(get_db)
):
    user_service.create_user_extra_info(user_request, db, user)
