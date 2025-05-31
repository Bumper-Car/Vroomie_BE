from app.crud import user_crud
from app.models.user import User
from app.schemas.user import UserScoreResponse


def get_user_score(user: User):
    return UserScoreResponse(score=user.user_score)


def create_user_extra_info(user_request, db, user):
    user = user_crud.create_user_extra_info(user_request, db, user)
    db.commit()
    return True