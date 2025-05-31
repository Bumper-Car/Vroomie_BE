from sqlalchemy.orm import Session

from app.crud import drive_tip_crud
from app.schemas.drive_tip import DriveTipsItem, DriveTipsResponse, DriveTipResponse


def get_drive_tips_title(db: Session):
    tips = drive_tip_crud.get_drive_tips_title(db)
    tips_item = [
        DriveTipsItem(
            tip_id=tip.tip_id,
            title=tip.title
        )
        for tip in tips
    ]
    return DriveTipsResponse(tips = tips_item)

def get_drive_tips(db: Session):
    tips = drive_tip_crud.get_drive_tips(db)
    tips_item = [
        DriveTipsItem(
            tip_id=tip.tip_id,
            title=tip.title,
            thumbnail_url=tip.thumbnail_url,
            create_at=tip.create_at
        )
        for tip in tips
    ]
    return DriveTipsResponse(tips = tips_item)


def get_drive_tip(db: Session, tip_id: int):
    tip = drive_tip_crud.get_drive_tip(db, tip_id)
    return DriveTipResponse(
        title = tip.title,
        thumbnail_url = tip.thumbnail_url,
        create_at = tip.create_at,
        content = tip.content,
    )
