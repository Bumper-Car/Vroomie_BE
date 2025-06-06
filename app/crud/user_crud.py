from sqlalchemy.orm import Session

from app.models import User
from app.schemas.user import UserExtraInfoRequest
from typing import Optional



def create_user_extra_info(user_request: UserExtraInfoRequest, db: Session, user: User) -> User:
    for key, value in user_request.model_dump().items():
        setattr(user, key, value)

    return user


def get_user_by_username(db: Session, username: str) -> Optional[User]:
    return db.query(User).filter(User.user_name == username).first()
