from datetime import datetime
from typing import List

from pydantic import BaseModel

class DriveHistoriesItem(BaseModel):
    history_id: int

    start_at: datetime
    end_at: datetime

    start_location: str
    end_location: str

    score: int

class DriveHistoriesResponse(BaseModel):
    histories: List[DriveHistoriesItem]

class VideoItem(BaseModel):
    video_id: str
    title: str
    content: str
    url: str

class DriveHistoryResponse(BaseModel):
    start_at: datetime
    end_at: datetime

    start_location: str
    end_location: str

    distance: float
    duration: int

    score: int

    lane_deviation_left_count: int
    lane_deviation_right_count: int
    safe_distance_violation_count: int
    sudden_deceleration_count: int
    sudden_acceleration_count: int
    speeding_count: int

    videos: List[VideoItem]

class DriveHistoryRequest(BaseModel):
    start_at: datetime
    end_at: datetime

    start_location: str
    end_location: str

    distance: float
    duration: int

    score: int

    lane_deviation_left_count: int
    lane_deviation_right_count: int
    safe_distance_violation_count: int
    sudden_deceleration_count: int
    sudden_acceleration_count: int
    speeding_count: int

    videos: List[VideoItem]