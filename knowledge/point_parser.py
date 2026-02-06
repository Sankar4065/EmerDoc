import re

def split_into_points(text: str) -> list[str]:
    """
    Robust splitter for LLM output.
    Respects newlines created during sanitization.
    """

    if not text or not text.strip():
        return []

    # 🔒 Normalize but PRESERVE newlines
    text = text.replace("\r", "\n")

    # 🔹 Primary split: newline-based
    raw_points = [
        p.strip()
        for p in text.split("\n")
        if p.strip()
    ]

    points = []

    for p in raw_points:
        # Remove leading numbering if present
        p = re.sub(r"^\d+\.\s*", "", p).strip()

        # Ignore tiny / junk fragments
        if len(p.split()) < 4:
            continue

        # Hard truncate to 30 words
        words = p.split()
        points.append(" ".join(words[:30]))

    return points
