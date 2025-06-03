from datetime import datetime
from collections import defaultdict
from app.models.drive_history import DriveHistory

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


def calculate_monthly_scores(histories: list[DriveHistory]) -> dict:
    monthly_scores = defaultdict(list)
    for h in histories:
        key = h.start_at.strftime("%Y-%m")
        monthly_scores[key].append(calculate_drive_score(h))

    return {
        month: round(sum(scores)/len(scores), 2)
        for month, scores in monthly_scores.items()
    }
