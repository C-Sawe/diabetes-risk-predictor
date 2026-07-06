from __future__ import annotations

# Band cutoffs on the predicted probability. Sensitivity-leaning: anything
# above 0.45 is escalated.
_LOW = 0.20
_MODERATE = 0.45
_HIGH = 0.75


def classify_risk(probability: float) -> dict:
    p = max(0.0, min(1.0, probability))

    if p < _LOW:
        return {
            "band": "Low",
            "tone": "ok",
            "action": "Routine monitoring. No immediate testing indicated.",
        }
    if p < _MODERATE:
        return {
            "band": "Moderate",
            "tone": "warn",
            "action": "Recheck within 6 months and watch for new or worsening symptoms.",
        }
    if p < _HIGH:
        return {
            "band": "High",
            "tone": "danger",
            "action": "Refer for a fasting blood glucose or HbA1c test soon.",
        }
    return {
        "band": "Very High",
        "tone": "danger",
        "action": "Prompt clinical review and diagnostic testing advised.",
    }
