from app.core.database import engine
from app.models.feedback import FeedbackLog
from app.core.database import Base

# 모든 모델을 포함한 테이블 생성
Base.metadata.create_all(bind=engine)

print("모든 테이블 생성 완료")
