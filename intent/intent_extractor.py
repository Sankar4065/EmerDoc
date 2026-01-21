import re

def extract_intent(query: str) -> list[str]:
    """
    Privacy-safe intent extraction.
    Removes tense/helper words like 'had'.
    """
    query = query.lower()
    words = re.findall(r"[a-z]+", query)

    stopwords = {
        "i", "me", "my",
        "had", "have", "having",
        "is", "am", "are", "was", "were",
        "the", "a", "an", "and", "or",
        "to", "of", "for", "with"
    }

    keywords = [
        w for w in words
        if w not in stopwords and len(w) > 3
    ]

    return list(dict.fromkeys(keywords))[:3]
