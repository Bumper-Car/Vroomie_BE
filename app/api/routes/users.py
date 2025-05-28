from fastapi import APIRouter, Header, Depends

from app.api.dependencies import get_user
from app.models.user import User
from app.schemas.user import UserScoreResponse
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