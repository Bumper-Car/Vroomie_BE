from app.crud import user_crud, drive_history_crud
from app.models.user import User
from app.schemas.user import UserScoreResponse, UserResponse, UserScoreReportResponse
from app.services import drive_score_service


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
        car_fuel = user.car_fuel,
        user_score = user.user_score,
    )

def get_user_score_report(db, user):
    # 1. 유저 이력 불러오기
    histories = drive_history_crud.get_histories(db, user)
    if not histories:
        return UserScoreReportResponse(
            score=0,
            percentile=0.0,
            percentile_distribution = {},
            monthly_scores={},
            monthly_detail_stats={}
        )

    # 전체 유저 user_score 가져오기
    all_users_scores = user_crud.get_all_users_score(db)

    # Percentile 계산용 점수 리스트 구성
    # 내 user_id는 무시하고, 내 점수는 한 번만 따로 넣기
    all_scores = [float(score) for uid, score in all_users_scores if uid != user.user_id]
    all_scores.append(float(user.user_score))

    percentile = drive_score_service.calculate_percentile(user.user_score, all_scores)

    # 6. percentile 분포 (그래프용)
    percentile_distribution = drive_score_service.calculate_percentile_distribution(all_scores)

    # 7. 월별 평균 점수 계산 (DB score 값 기준)
    monthly_scores = drive_score_service.calculate_monthly_scores(histories)

    # 8. 월별 상세 통계
    monthly_detail_stats = drive_score_service.calculate_monthly_detail_stats(histories)

    return UserScoreReportResponse(
        score=user.user_score,
        percentile=percentile,
        percentile_distribution=percentile_distribution,
        monthly_scores=monthly_scores,
        monthly_detail_stats=monthly_detail_stats,
    )
