from typing import Any

DIMENSIONS = [
    "pain",
    "frequency",
    "time_loss",
    "money_loss",
    "urgency",
    "market_size",
    "willingness_to_pay",
    "current_solution_weakness",
    "existing_spend",
    "ease_of_solving",
    "retention",
    "competitive_gap",
]

def score_problem(
    problem: str,
    pain: dict[str, Any],
    frequency: dict[str, Any],
    time_loss: dict[str, Any],
    money_loss: dict[str, Any],
    urgency: dict[str, Any],
    market_size: dict[str, Any],
    willingness_to_pay: dict[str, Any],
    current_solution_weakness: dict[str, Any],
    existing_spend: dict[str, Any],
    ease_of_solving: dict[str, Any],
    retention: dict[str, Any],
    competitive_gap: dict[str, Any],
) -> dict[str, Any]:
    """
    Deterministically score a business problem.

    Every dimension must contain:
      - score: integer from 1 to 5
      - evidence: concise evidence supporting the score
    """
    values = {
        "pain": pain,
        "frequency": frequency,
        "time_loss": time_loss,
        "money_loss": money_loss,
        "urgency": urgency,
        "market_size": market_size,
        "willingness_to_pay": willingness_to_pay,
        "current_solution_weakness": current_solution_weakness,
        "existing_spend": existing_spend,
        "ease_of_solving": ease_of_solving,
        "retention": retention,
        "competitive_gap": competitive_gap,
    }

    for name, item in values.items():
        if not isinstance(item, dict):
            raise ValueError(f"{name} must be an object")

        score = item.get("score")
        evidence = item.get("evidence")

        if not isinstance(score, int) or not 1 <= score <= 5:
            raise ValueError(f"{name}.score must be an integer from 1 to 5")

        if not isinstance(evidence, str) or not evidence.strip():
            raise ValueError(f"{name}.evidence is required")

    total_score = sum(item["score"] for item in values.values())

    if total_score >= 48:
        priority = "VERY_HIGH"
    elif total_score >= 36:
        priority = "HIGH"
    elif total_score >= 24:
        priority = "MEDIUM"
    else:
        priority = "LOW"

    return {
        "problem": problem,
        "total_score": total_score,
        "max_score": 60,
        "priority": priority,
        "dimensions": values,
    }
