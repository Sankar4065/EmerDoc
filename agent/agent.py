from intent.intent_extractor import extract_intent
from knowledge.llm_generator import generate_knowledge
from knowledge.point_parser import split_into_points
from knowledge.knowledge_limiter import limit_knowledge
from knowledge.safety import (
    is_action_point,
    is_safe_first_aid,
    normalize_point
)

from memory.temp_memory import (
    init_collection,
    store_temp_knowledge,
    retrieve_temp_knowledge
)

from memory.long_term_memory import (
    init_long_term_collection,
    store_long_term_memory,
    retrieve_long_term_memory
)

from agent.context_builder import build_context
from agent.reasoning import reason
from agent.reasoning_utils import (
    rerank_with_past_memory,
    remove_repeated_advice
)



BLOCKED_PREFIXES = (
    "what is",
    "types of",
    "causes of",
    "symptoms of",
    "headache is",
    "headaches are",
    "diet and",
    "stress and",
    "overuse of",
    "tension headaches",
    "sinus headaches",
    "migraine headaches",
    "general first-aid",
    "general safety"
)



def run_agent(query: str, user_id: str):
    print("\n================= NEW QUERY =================")
    print("USER QUERY:", query)
    print("============================================\n")

    # 1️⃣ Init memory
    init_collection()
    init_long_term_collection()

    # 2️⃣ Extract intent
    intent = extract_intent(query)
    print("INTENT:", intent, "\n")

    # 3️⃣ Generate LLM knowledge (internal only)
    raw_knowledge = generate_knowledge(intent)
    print("RAW LLM OUTPUT:\n", raw_knowledge, "\n")

    # 4️⃣ Split into candidate points
    points = split_into_points(raw_knowledge)

    print("STORING SAFE ACTION POINTS:\n")

    # 5️⃣ STRICT + CORRECT FILTERING
    for p in points:
        clean = normalize_point(p)

        if clean.startswith(BLOCKED_PREFIXES):
            continue

        if is_action_point(clean) and is_safe_first_aid(clean):
            clean = limit_knowledge(clean, max_words=25)
            print("✔", clean)
            store_temp_knowledge(clean)

    # 6️⃣ Long-term memory (REASONING ONLY)
    past_memory = retrieve_long_term_memory(query)
    print("PAST MEMORY (FOR REASONING ONLY):\n", past_memory, "\n")

    # 7️⃣ Vector retrieval (ANSWER SOURCE)
    retrieved = rerank_with_past_memory(
        retrieve_temp_knowledge(query),
        past_memory
    )

    retrieved = remove_repeated_advice(retrieved, past_memory)

    print("\nRETRIEVED ANSWER:\n", retrieved, "\n")

    # 8️⃣ Store learning
    store_long_term_memory(
        text=query,
        category="user_query"
    )

    for p in retrieved:
        store_long_term_memory(
            text=p,
            category="validated_first_aid"
        )

    # 9️⃣ Context + reasoning
    context = build_context(
        retrieved_points=retrieved,
        intent=intent,
        past_memory=past_memory
    )

    return reason(context)

