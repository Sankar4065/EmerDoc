from agents.base import Agent

from memory.temp_memory import (
    store_temp_knowledge,
    retrieve_temp_knowledge
)

from memory.long_term_memory import (
    create_episode,
    store_episode,
    retrieve_latest_episode
)

from memory.personal_data import store_personal_medical_data
from memory.input_time_tracker import InputTimeTracker

time_tracker = InputTimeTracker()


class MemoryAgent(Agent):
    def run(self, context: dict) -> dict:
        if context["stage"] != 4:
            return context

        print("Memory agent running...")

        user_id = context["user_id"]
        query = context["query"]
        validated = context.get("validated_points", [])

        # -------------------------------------------------
        # SHORT-TERM MEMORY
        # -------------------------------------------------
        for p in validated:
            print("[DEBUG][MEMORY] Temp store →", p)
            store_temp_knowledge(p)

        top_points = retrieve_temp_knowledge(query, limit=3)
        print("[DEBUG][MEMORY] Retrieved temp →", top_points)

        # -------------------------------------------------
        # EPISODIC MEMORY
        # -------------------------------------------------
        gap = time_tracker.check_time_gap()

        episode = (
            retrieve_latest_episode(user_id)
            if gap == "less_than_30_minutes"
            else None
        )

        if episode is None:
            episode = create_episode(user_id)

        for p in top_points:
            if p not in episode["care_suggestions"]:
                episode["care_suggestions"].append(p)

        store_episode(episode)

        # -------------------------------------------------
        # 🔥 PERSONAL MEMORY STORE (FINAL)
        # -------------------------------------------------
        print("[DEBUG][PERSONAL] Storing personal data")

        store_personal_medical_data(
            name=user_id,
            symptoms=context.get("symptoms", []),
            cause=None,
            issue=context.get("issue"),
            care_suggestions=top_points
        )

        # -------------------------------------------------
        # OUTPUT
        # -------------------------------------------------
        context["retrieved"] = top_points
        context["past_memory"] = [episode]

        print("[DEBUG][MEMORY] Done")

        return context
