def rerank_with_past_memory(retrieved, past_memory):
    if not past_memory:
        return retrieved

    boosted = []
    others = []

    past_text = " ".join(past_memory).lower()

    for p in retrieved:
        if any(word in past_text for word in p.lower().split()):
            boosted.append(p)
        else:
            others.append(p)

    return boosted + others


def remove_repeated_advice(retrieved, past_memory):
    past = set(p.lower() for p in past_memory)
    return [p for p in retrieved if p.lower() not in past]    
