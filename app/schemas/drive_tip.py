from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel

class DriveTipsItem(BaseModel):
    tip_id: int
    title: str
    thumbnail_url: Optional[str] = None
    create_at: Optional[datetime] = None

class DriveTipsResponse(BaseModel):
    tips: List[DriveTipsItem]

class DriveTipResponse(BaseModel):
    tip_id: int
    title: str
    thumbnail_url: str = None
    create_at: datetime = None
    content: str