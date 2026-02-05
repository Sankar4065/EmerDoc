# from modality.modality_router import normalize_input

# from intent.intent_extractor import extract_intent
# from knowledge.llm_generator import generate_knowledge
# from knowledge.point_parser import split_into_points
# from knowledge.knowledge_limiter import limit_knowledge
# from knowledge.safety import (
#     is_action_point,
#     is_safe_first_aid,
#     normalize_point
# )

# from memory.temp_memory import (
#     init_collection,
#     store_temp_knowledge,
#     retrieve_temp_knowledge
# )

# from memory.long_term_memory import (
#     init_long_term_collection,
#     store_long_term_memory,
#     retrieve_long_term_memory
# )

# from agent.context_builder import build_context
# from agent.reasoning import reason
# from agent.reasoning_utils import (
#     rerank_with_past_memory,
#     remove_repeated_advice
# )


# AGENT_ROLES = {
#     "planner": "intent_extractor",
#     "generator": "knowledge_generator",
#     "critic": "safety_filter",
#     "retriever": "vector_memory",
#     "executor": "reasoning_engine"
# }


# BLOCKED_PREFIXES = (
#     "what is",
#     "types of",
#     "causes of",
#     "symptoms of",
#     "headache is",
#     "headaches are",
#     "diet and",
#     "stress and",
#     "overuse of",
#     "tension headaches",
#     "sinus headaches",
#     "migraine headaches",
#     "general first-aid",
#     "general safety"
# )


# def planner_decision(intent: list[str]) -> bool:
#     """
#     Planner agent decides whether retrieval is needed.
#     """
#     return len(intent) > 0


# # def run_agent(
# #     query: str | None = None,
# #     user_id: str = "default",
# #     image_path: str | None = None,
# #     audio_path: str | None = None
# # ):
# #     print("\n================= NEW QUERY =================")

# #     # 🔹 Normalize multimodal input → TEXT
# #     query = normalize_input(
# #         text=query,
# #         image_path=image_path,
# #         audio_path=audio_path
# #     )

# #     if not query:
# #         return "No valid input provided."

# #     print("NORMALIZED QUERY:", query)
# #     print("============================================\n")

# #     # 1️⃣ Init memory
# #     init_collection()
# #     init_long_term_collection()

# #     # 2️⃣ Intent extraction
# #     intent = extract_intent(query)
# #     print("INTENT:", intent, "\n")

# #     # 3️⃣ Internal LLM generation
# #     raw_knowledge = generate_knowledge(intent)
# #     print("RAW LLM OUTPUT:\n", raw_knowledge, "\n")

# #     # 4️⃣ Split into points
# #     points = split_into_points(raw_knowledge)

# #     print("STORING SAFE ACTION POINTS:\n")

# #     # 5️⃣ Strict filtering
# #     for p in points:
# #         clean = normalize_point(p)

# #         if clean.startswith(BLOCKED_PREFIXES):
# #             continue

# #         if is_action_point(clean) and is_safe_first_aid(clean):
# #             clean = limit_knowledge(clean, max_words=25)
# #             print("✔", clean)
# #             store_temp_knowledge(clean)

# #     # 6️⃣ Past memory (reasoning only)
# #     past_memory = retrieve_long_term_memory(query)
# #     print("PAST MEMORY:\n", past_memory, "\n")

# #     # 7️⃣ Retrieval + reranking
# #     retrieved = rerank_with_past_memory(
# #         retrieve_temp_knowledge(query),
# #         past_memory
# #     )

# #     retrieved = remove_repeated_advice(retrieved, past_memory)

# #     print("RETRIEVED ANSWER:\n", retrieved, "\n")

# #     # 8️⃣ Store learning
# #     store_long_term_memory(text=query, category="user_query")

# #     for p in retrieved:
# #         store_long_term_memory(text=p, category="validated_first_aid")

# #     # 9️⃣ Reasoning
# #     context = build_context(
# #         retrieved_points=retrieved,
# #         intent=intent,
# #         past_memory=past_memory
# #     )

# #     return reason(context)
