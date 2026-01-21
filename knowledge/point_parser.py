import re

def split_into_points(text: str) -> list[str]:
    """
    Robust splitter for LLM output.
    Handles numbered, inline, and paragraph outputs.
    """
    text = re.sub(r"\s+", " ", text).strip()

    raw_points = re.split(r"\s*\d+\.\s*", text)

    points = []

    for p in raw_points:
        p = p.strip()
        if len(p) < 25:
            continue

        words = p.split()
        points.append(" ".join(words[:30]))

    return points
