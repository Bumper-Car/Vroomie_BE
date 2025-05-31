from fastapi import APIRouter

from app.api.routes import gpt, drive, login, users, drive_history, drive_tip

router = APIRouter()
router.include_router(login.router)
router.include_router(drive.router)
router.include_router(gpt.router)
router.include_router(users.router)
router.include_router(drive_history.router)
router.include_router(drive_tip.router)
