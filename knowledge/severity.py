# ==================================================
# SEVERITY RANKING
# ==================================================

SEVERITY_RANK = {
    # =========================
    # VERY MILD / IRRITATION
    # =========================
    "throatirritation": 0,
    "drythroat": 0,
    "mildcough": 0,
    "allergy": 0,
    "seasonalallergy": 0,

    # =========================
    # MILD (COMMON, SELF-LIMITING)
    # =========================
    "commoncold": 1,
    "headcold": 1,
    "nasalcongestion": 1,
    "runnynose": 1,
    "sneezing": 1,
    "cough": 1,
    "drycough": 1,
    "postnasaldrip": 1,
    "sorethroat": 1,

    # =========================
    # MODERATE (SYSTEMIC / PROLONGED)
    # =========================
    "infection": 2,
    "viralinfection": 2,
    "flu": 2,
    "influenza": 2,
    "bronchitis": 2,
    "chestinfection": 2,
    "persistentcough": 2,
    "wetcough": 2,
    "productivecough": 2,
    "fever": 2,
    "highfever": 2,

    # =========================
    # SEVERE (ESCALATION REQUIRES SUPPORT)
    # =========================
    "pneumonia": 3,
    "severechestinfection": 3,
    "shortnessofbreath": 3,
    "breathingdifficulty": 3,
    "respiratorydistress": 3,
    "covid": 3,
    "covid19": 3,
}


# ==================================================
# MINIMUM SYMPTOMS REQUIRED FOR ESCALATION
# ==================================================

ISSUE_SYMPTOM_REQUIREMENTS = {
    "pneumonia": {
        "fever",
        "chest pain",
        "shortness of breath",
        "productive cough"
    },
    "flu": {
        "fever",
        "body ache",
        "fatigue"
    },
}


# ==================================================
# ESCALATION GUARD
# ==================================================

def should_escalate_issue(
    previous_issue: str | None,
    new_issue: str,
    symptoms: list[str]
) -> bool:
    """
    Prevents unsafe medical escalation.
    """

    # First issue → always allow
    if previous_issue is None:
        return True

    # Unknown previous issue → allow downgrade
    if previous_issue not in SEVERITY_RANK:
        return True

    prev_rank = SEVERITY_RANK.get(previous_issue, 0)
    new_rank = SEVERITY_RANK.get(new_issue, 0)

    # Downgrade or same level → allow
    if new_rank <= prev_rank:
        return True

    # Escalation requires symptom support
    required = ISSUE_SYMPTOM_REQUIREMENTS.get(new_issue)
    if not required:
        return False  # unknown escalation = block

    symptom_set = set(s.lower() for s in symptoms)

    # Require at least ONE strong supporting symptom
    if symptom_set.intersection(required):
        return True

    return False
