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