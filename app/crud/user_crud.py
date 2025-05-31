from sqlalchemy.orm import Session

from app.models import User
from app.schemas.user import UserExtraInfoRequest


def create_user_extra_info(user_request: UserExtraInfoRequest, db: Session, user: User) -> User:
    for key, value in user_request.model_dump().items():
        setattr(user, key, value)

    return user
