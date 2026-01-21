def build_context(retrieved_points, intent, past_memory):
    return {
        "intent": intent,
        "retrieved_points": retrieved_points,  # used for answer
        "past_memory": past_memory              # used for reasoning
    }
