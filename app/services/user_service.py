from app.models.user import User
from app.schemas.user import UserScoreResponse


def get_user_score(user: User):
    return UserScoreResponse(score=user.user_score)