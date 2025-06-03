import os
from fastapi import APIRouter, Request, Header, HTTPException, Depends
from sqlalchemy.orm import Session
from starlette.responses import RedirectResponse

from app.services.auth_service import kakao_login, get_user_by_token
from app.core.database import get_db

router = APIRouter(prefix="/auth", tags=["login"])

# Android 앱용 딥링크
REDIRECT_SCHEME = os.getenv("APP_REDIRECT_SCHEME", "vroomie://login-success")

@router.get("/kakao/callback")
def kakao_callback(request: Request, db: Session = Depends(get_db)):
    code = request.query_params.get("code")
    if not code:
        raise HTTPException(status_code=400, detail="Missing 'code' in query parameters")
    try:
        user_info = kakao_login(code, db)
        token = user_info["token"]
        return RedirectResponse(url=f"{REDIRECT_SCHEME}?token={token}")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/me")
def get_me(authorization: str = Header(...), db: Session = Depends(get_db)):
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid token format")
    token = authorization[7:]
    user = get_user_by_token(token, db)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return user