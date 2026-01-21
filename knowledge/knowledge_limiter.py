def limit_knowledge(text: str, max_words: int = 25) -> str:
    """
    Per-point safety limiter.
    """
    words = text.split()
    return " ".join(words[:max_words])
