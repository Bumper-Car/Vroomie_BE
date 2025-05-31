from app.core.database import engine
from app.models.feedback import FeedbackLog
from app.models.user import User
from app.models.drive_history import DriveHistory
from app.models.drive_history_video import DriveHistoryVideo
from app.models.drive_statistic import DriveStatistic
from app.models.drive_tip import DriveTip
from app.core.database import Base

# 모든 모델을 포함한 테이블 생성
Base.metadata.create_all(bind=engine)

print("모든 테이블 생성 완료")
