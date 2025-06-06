from typing import Dict, OrderedDict, List

from pydantic import BaseModel

from app.models.user import CarTypeEnum, FuelTypeEnum


class UserScoreResponse(BaseModel):
    score: int

class UserExtraInfoRequest(BaseModel):
    user_name: str = None
    car_model: str = None
    car_hipass: bool = None
    car_type: CarTypeEnum = None
    car_fuel: FuelTypeEnum = None

class UserResponse(BaseModel):
    user_name: str = None
    car_model: str = None
    car_hipass: bool = None
    car_type: CarTypeEnum = None
    car_fuel: FuelTypeEnum = None
    user_score: int = None

class MonthlyDetailStat(BaseModel):
    average_score: int
    total_distance: float
    total_duration: int
    total_speeding_count: int
    total_sudden_acceleration_count: int
    total_sudden_deceleration_count: int
    total_safe_distance_violation_count: int
    total_lane_deviation_right_count: int
    total_lane_deviation_left_count: int

class MonthlyScoreItem(BaseModel):
    year: int
    month: int
    score: int

class UserScoreReportResponse(BaseModel):
    score: int
    percentile: float
    percentile_distribution: Dict[int, int]
    monthly_scores: List[MonthlyScoreItem]
    monthly_detail_stats: Dict[int, MonthlyDetailStat]
