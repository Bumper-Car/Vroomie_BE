from sqlalchemy.orm import Session

from app.models import User
from app.schemas.user import UserExtraInfoRequest


def create_user_extra_info(user_request: UserExtraInfoRequest, db: Session, user: User) -> User:
    for key, value in user_request.model_dump().items():
        setattr(user, key, value)

    return user

def get_all_users_score(db: Session):
    return (db.query(User.user_id, User.user_score)
            .filter(User.user_score.isnot(None))
            .all())

def update_user_score(db: Session, user_id: int, user_score: int):
    (db.query(User)
     .filter(User.user_id == user_id)
     .update({User.user_score: user_score}))