from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel
from app.core.database import get_db
from app.models import drive_history_video
from app.api.dependencies import get_user

router = APIRouter(prefix="/drive/video", tags=["drive"])

# result 값에 따른 메시지 자동 매핑
result_to_message_map = {
    "Left_Deviation": {
        "title": "좌측 차선 이탈에 주의하세요",
        "content": "차량이 좌측 차선을 이탈했습니다. 핸들을 중앙으로 유지하는 연습이 필요합니다."
    },
    "Right_Deviation": {
        "title": "우측 차선 이탈에 주의하세요",
        "content": "차량이 우측 차선을 이탈했습니다. 오른발을 도로의 중앙에 맞추는 습관을 들이세요."
    },
    "Cut_In": {
        "title": "끼어들기 상황 감지",
        "content": "우측 또는 좌측 차량이 차로를 변경하려고 합니다. 속도를 줄여서 끼어들 공간을 확보해주세요."
    },
    "Safe_Distance_Violation": {
        "title": "안전거리 미확보가 감지되었습니다",
        "content": "앞차와의 거리를 충분히 유지해주세요. 추돌 위험이 있습니다."
    },
    "Stopped_Distance_Check": {
        "title": "정지 시 거리 확인 필요",
        "content": "정지 시 앞차와의 거리를 충분히 확보했는지 확인해주세요."
    }
}

class DriveVideoCreate(BaseModel):
    user_id: int
    history_id: int
    s3_url: str
    result: str  # "Left_Deviation", "Cut_In" 등

@router.post("/save")
def save_drive_video_clips(
    videos: List[DriveVideoCreate],
    db: Session = Depends(get_db)
):
    for video in videos:
        mapping = result_to_message_map.get(video.result, {})
        title = mapping.get("title", f"{video.result} 상황")
        content = mapping.get("content", "운전 중 발생한 이벤트 기반 영상입니다.")

        db_video = drive_history_video.DriveHistoryVideo(
            user_id=video.user_id,
            history_id=video.history_id,
            title=title,
            content=content,
            video_url=video.s3_url,
        )
        db.add(db_video)

    db.commit()
    return {"message": f"{len(videos)}개의 영상이 저장되었습니다."}


class DriveVideoOut(BaseModel):
    history_video_id: int
    user_id: int
    history_id: int
    title: str
    content: str
    video_url: str

    class Config:
        orm_mode = True

@router.get("/{history_id}", response_model=List[DriveVideoOut])
def get_drive_video_clips(
    history_id: int,
    db: Session = Depends(get_db),
    user = Depends(get_user),
):
    videos = db.query(drive_history_video.DriveHistoryVideo)\
        .filter(
            drive_history_video.DriveHistoryVideo.history_id == history_id,
            drive_history_video.DriveHistoryVideo.user_id == user.user_id
        )\
        .all()

    if not videos:
        raise HTTPException(status_code=404, detail="해당 주행에 대한 영상이 없습니다.")

    return videos
