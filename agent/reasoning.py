def reason(context):
    """
    Reasoning may internally consider past_memory,
    but the final answer must ONLY come from retrieved_points.
    """

    # Example reasoning hook (future use)
    _ = context.get("past_memory", [])

    return {
        "answer": context["retrieved_points"],
        "used_intent": context["intent"],
        "past_memory_used": context.get("past_memory", []),
        "source": "qdrant_vector_search"
    }
