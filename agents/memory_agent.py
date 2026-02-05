from agents.base import Agent
from memory.temp_memory import store_temp_knowledge, retrieve_temp_knowledge
from memory.long_term_memory import retrieve_long_term_memory

class MemoryAgent(Agent):
    def run(self, context: dict) -> dict:
        if context["stage"] != 4:
            return context

        print("Memory agent running...")
        query = context["query"]

        print(f"[DEBUG][MEMORY] Storing validated points → {len(context['validated_points'])}")
        for p in context["validated_points"]:
            print("  → storing:", p)
            store_temp_knowledge(p)

        context["past_memory"] = retrieve_long_term_memory(query)
        print(f"[DEBUG][MEMORY] Long-term hits → {len(context['past_memory'])}")

        context["retrieved"] = retrieve_temp_knowledge(query)
        print(f"[DEBUG][MEMORY] Temp retrieved → {len(context['retrieved'])}")

        return context
