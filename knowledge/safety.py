import re

# verbs that indicate ACTION
ACTION_VERBS = (
    "apply",
    "drink",
    "rest",
    "avoid",
    "stay",
    "use",
    "massage",
    "relax",
    "keep",
    "encourage",
    "ensure",
    "maintain",
    "limit",
    "reduce",
    "get"
)

# block unsafe medical content
BANNED_TERMS = (
    "medicine",
    "medication",
    "tablet",
    "pill",
    "ibuprofen",
    "acetaminophen",
    "prescription",
    "diagnosis",
    "disease",
    "epipen",
    "cpr",
    "antibiotic"
)

# block generic safety / unrelated actions
GENERIC_FIRST_AID = (
    "use gloves",
    "wash hands",
    "epipen",
    "cpr",
    "call emergency",
    "monitor vital",
    "blood pressure"
)


def normalize_point(text: str) -> str:
    """
    Remove markdown, headings, numbering.
    """
    text = text.lower()

    # remove markdown
    text = re.sub(r"\*\*(.*?)\*\*", "", text)

    # remove numbering
    text = re.sub(r"^\d+\.\s*", "", text)

    # normalize whitespace
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def is_action_point(text: str) -> bool:
    """
    Accept if sentence CONTAINS an action verb,
    not necessarily starts with it.
    """
    t = normalize_point(text)

    if any(g in t for g in GENERIC_FIRST_AID):
        return False

    return any(v in t for v in ACTION_VERBS)


def is_safe_first_aid(text: str) -> bool:
    t = normalize_point(text)
    return not any(b in t for b in BANNED_TERMS)
