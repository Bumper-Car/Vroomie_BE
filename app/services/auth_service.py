from datetime import datetime, timedelta
from sqlalchemy.orm import Session
import os
import jwt

from app.models.user import User
from app.core.kakao_client import get_kakao_token, get_kakao_user_info

SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your_jwt_secret")
ALGORITHM = "HS256"


def create_jwt_token(data: dict, expires_delta: timedelta = timedelta(hours=1)) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_jwt_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.PyJWTError:
        return None


def kakao_login(code: str, db: Session):
    access_token = get_kakao_token(code)
    user_info = get_kakao_user_info(access_token)

    kakao_id = str(user_info.get("id"))
    nickname = user_info.get("properties", {}).get("nickname", "")

    user = db.query(User).filter_by(kakao_id=kakao_id).first()
    if not user:
        user = User(
            kakao_id=kakao_id,
            user_name=nickname,
            create_at=datetime.utcnow()
        )
        db.add(user)
        db.commit()
        db.refresh(user)

    token = create_jwt_token({"user_id": user.user_id})
    return {
        "token": token,
        "user_id": user.user_id,
        "user_name": user.user_name,
    }


def get_user_by_token(token: str, db: Session):
    payload = decode_jwt_token(token)
    if not payload:
        return None
    user_id = payload.get("user_id")
    return db.query(User).filter_by(user_id=user_id).first()