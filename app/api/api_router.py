from fastapi import APIRouter

from app.api.routes import gpt, drive, login

router = APIRouter()
router.include_router(login.router)
router.include_router(drive.router)
router.include_router(gpt.router)
