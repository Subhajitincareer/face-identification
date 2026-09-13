from typing import Any

def rank_problems(
    problems: list[dict[str, Any]],
    top_n: int = 10,
) -> dict[str, Any]:
    """
    Rank scored business problems by total score.

    Returns the top N opportunities.
    """
    if not isinstance(top_n, int) or top_n < 1:
        raise ValueError("top_n must be a positive integer")

    valid_problems = [
        p for p in problems
        if isinstance(p, dict) and "total_score" in p
    ]

    ranked = sorted(
        valid_problems,
        key=lambda p: p["total_score"],
        reverse=True,
    )

    return {
        "count": len(ranked),
        "top_n": min(top_n, len(ranked)),
        "ranked_problems": ranked[:top_n],
    }
