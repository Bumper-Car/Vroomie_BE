from collections import defaultdict
from datetime import datetime
from typing import Dict

from dateutil.relativedelta import relativedelta
from sqlalchemy.orm import Session

from app.crud import drive_history_crud
from app.models import User
from app.models.drive_history import DriveHistory
from app.schemas.user import MonthlyDetailStat, MonthlyScoreItem

def calculate_drive_score(history: DriveHistory) -> float:
    if not history.distance or history.distance == 0:
        return 0.0

    distance_unit = max(history.distance / 100, 1.0)
    danger_penalty = (
        history.speeding_count +
        history.sudden_acceleration_count +
        history.sudden_deceleration_count
    ) / distance_unit * 5.0

    rule_penalty = (
        (history.lane_deviation_left_count or 0) * 2 +
        (history.lane_deviation_right_count or 0) * 2 +
        (history.safe_distance_violation_count or 0) * 2
    )

    total_penalty = danger_penalty + rule_penalty
    return round(max(100.0 - total_penalty, 0.0), 2)


def calculate_percentile(user_score: float, all_scores: list[float]) -> float:

    if not all_scores:
        return 0.0

    if len(all_scores) == 1:
        return 100.0

    below = sum(1 for score in all_scores if score < user_score)
    return round((below / len(all_scores)) * 100, 2) if all_scores else 0.0


def calculate_monthly_scores(histories: list[DriveHistory]) -> list[MonthlyScoreItem]:
    monthly_scores = defaultdict(list)
    for h in histories:
        key = (h.start_at.year, h.start_at.month)
        monthly_scores[key].append(calculate_drive_score(h))

    today = datetime.today()
    recent_keys = [
        ((today - relativedelta(months=i)).year, (today - relativedelta(months=i)).month)
        for i in range(6)
    ]

    result = []

    for (year, month) in sorted(recent_keys):
        scores = monthly_scores.get((year, month), [])
        if scores:
            avg_score = int(round(sum(scores) / len(scores), 2))
        else:
            avg_score = 0

        result.append(MonthlyScoreItem(
            year=year,
            month=month,
            score=avg_score
        ))

    return result

def calculate_percentile_distribution(all_scores: list[float]) -> Dict[int, int]:    # 초기화: 0~100 점수 구간 만들기 (처음에 전부 count = 0)
    distribution = {score: 0 for score in range(0, 101)}  # 0 ~ 100 포함

    # 점수 집계
    for score in all_scores:
        bucket = int(score)
        if 0 <= bucket <= 100:  # 안전하게 범위 체크 (혹시 잘못된 값 방지)
            distribution[bucket] += 1

    return distribution


def calculate_monthly_detail_stats(histories: list[DriveHistory]) -> Dict[int, MonthlyDetailStat]:
    monthly_data = defaultdict(list)

    for h in histories:
        key = (h.start_at.year, h.start_at.month)
        monthly_data[key].append(h)

    # 최근 6개월 key 생성
    today = datetime.today()
    recent_keys = [
        ((today - relativedelta(months=i)).year, (today - relativedelta(months=i)).month)
        for i in range(6)
    ]

    result = {}
    for year, month in recent_keys:
        records = monthly_data.get((year, month))

        if records:
            average_score = (
                sum(h.score for h in records if h.score is not None) / len(records)
                if records else 0.0
            )
            total_distance = sum(h.distance or 0 for h in records)
            total_duration = sum(h.duration or 0 for h in records)
            total_speeding = sum(h.speeding_count or 0 for h in records)
            total_sudden_acceleration = sum(h.sudden_acceleration_count or 0 for h in records)
            total_sudden_deceleration = sum(h.sudden_deceleration_count or 0 for h in records)
            total_safe_distance_violation = sum(h.safe_distance_violation_count or 0 for h in records)
            total_lane_deviation_right = sum(h.lane_deviation_right_count or 0 for h in records)
            total_lane_deviation_left = sum(h.lane_deviation_left_count or 0 for h in records)
        else:
            average_score = 0.0
            total_distance = 0.0
            total_duration = 0
            total_speeding = 0
            total_sudden_acceleration = 0
            total_sudden_deceleration = 0
            total_safe_distance_violation = 0
            total_lane_deviation_right = 0
            total_lane_deviation_left = 0

        result[month] = MonthlyDetailStat(
            average_score=int(round(average_score, 2)),
            total_distance=round(total_distance, 2),
            total_duration=int(round(total_duration, 0)),
            total_speeding_count=total_speeding,
            total_sudden_acceleration_count=total_sudden_acceleration,
            total_sudden_deceleration_count=total_sudden_deceleration,
            total_safe_distance_violation_count=total_safe_distance_violation,
            total_lane_deviation_right_count=total_lane_deviation_right,
            total_lane_deviation_left_count=total_lane_deviation_left
        )

    return result

def calculate_user_score(db: Session, user: User) -> int:
    recent_scores = drive_history_crud.get_my_recent_histories_score(db, user.user_id)

    if not recent_scores:
        return 0

    total_score = sum(h.score for h in recent_scores)
    average_score = total_score / len(recent_scores)
    return round(average_score)