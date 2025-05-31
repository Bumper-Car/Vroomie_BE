from app.crud import user_crud
from app.models.user import User
from app.schemas.user import UserScoreResponse, UserResponse


def get_user_score(user: User):
    return UserScoreResponse(score=user.user_score)


def create_user_extra_info(user_request, db, user):
    user = user_crud.create_user_extra_info(user_request, db, user)
    db.commit()
    return True


def get_user(user):
    return UserResponse(
        user_name = user.user_name,
        car_model = user.car_model,
        car_hipass = user.car_hipass,
        car_type = user.car_type,
        car_fuel = user.car_fuel
    )