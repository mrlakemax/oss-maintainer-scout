from __future__ import annotations

from .models import ScanResult, ScoreResult


def score_scan(scan: ScanResult) -> ScoreResult:
    total_points = sum(check.weight for check in scan.checks)
    earned_points = sum(check.weight for check in scan.checks if check.passed)
    score = round((earned_points / total_points) * 100) if total_points else 0
    missing_required = [check.id for check in scan.checks if check.required and not check.passed]
    recommendations = [
        check.recommendation
        for check in scan.checks
        if check.required and not check.passed
    ]

    return ScoreResult(
        earned_points=earned_points,
        total_points=total_points,
        score=score,
        grade=_grade(score),
        missing_required_ids=missing_required,
        recommendations=recommendations,
    )


def _grade(score: int) -> str:
    if score >= 90:
        return "A"
    if score >= 80:
        return "B"
    if score >= 70:
        return "C"
    if score >= 60:
        return "D"
    return "F"
