from typing import List

from sqlalchemy import select
from sqlalchemy.orm import Session, load_only

from app.models.drive_tip import DriveTip

def get_drive_tips_title(db: Session) -> List[DriveTip]:
    return list(
        db.scalars(
            select(DriveTip).options(
                load_only(
                    DriveTip.tip_id,
                    DriveTip.title
                )
            )
            .order_by(DriveTip.create_at.desc())
            .limit(5)
        )
        .all()
    )


def get_drive_tips(db: Session) -> List[DriveTip]:
    return list(
        db.scalars(
            select(DriveTip)
        )
        .all()
    )