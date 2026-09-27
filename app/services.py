from app.models import Inspection


def health_score(inspection: Inspection) -> int:
    score = 0
    if inspection.queen_seen:
        score += 2
    score += {"forte": 2, "regular": 1, "fraco": 0}.get(inspection.brood_pattern, 0)
    if not inspection.pest_signs:
        score += 1
    if inspection.temperament == "calmo":
        score += 1
    return score
