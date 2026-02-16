"""
Placeholder health score logic: shading and current threshold reduce score.
Designed for easy replacement by ML later.
"""
# Penalties (tunable)
PENALTY_SHADING = 35
PENALTY_LOW_CURRENT = 25
CURRENT_THRESHOLD_DEFAULT = 1.5  # A below which we penalize


def compute_health_score(
    current_a: float,
    shading_active: bool,
    current_threshold: float = CURRENT_THRESHOLD_DEFAULT,
) -> float:
    """
    Return a 0-100 health score.
    Base 100; subtract for shading and for current below threshold.
    """
    score = 100.0
    if shading_active:
        score -= PENALTY_SHADING
    if current_a < current_threshold:
        score -= PENALTY_LOW_CURRENT
    return max(0.0, min(100.0, round(score, 1)))
