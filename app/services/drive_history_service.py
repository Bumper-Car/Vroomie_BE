from sqlalchemy.orm import Session

from app.crud import drive_history_crud
from app.models.user import User


def get_drive_histories(db: Session, user: User):
    return drive_history_crud.get_histories(db, user)
