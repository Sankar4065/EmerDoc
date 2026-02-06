from agents.base import Agent
from memory.temp_memory import store_temp_knowledge, retrieve_temp_knowledge
from memory.long_term_memory import create_episode, store_episode, retrieve_latest_episode
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

        # ---------------- TEMP MEMORY ----------------
        for p in validated:
            store_temp_knowledge(p)

        top = retrieve_temp_knowledge(query, limit=3)
        print("[DEBUG][MEMORY] Retrieved temp →", top)

        # ---------------- EPISODE ----------------
        gap = time_tracker.check_time_gap()
        episode = (
            retrieve_latest_episode(user_id)
            if gap == "less_than_30_minutes"
            else None
        )

        if episode is None:
            episode = create_episode(user_id)

        for p in top:
            if p not in episode["care_suggestions"]:
                episode["care_suggestions"].append(p)

        store_episode(episode)

        # 🔥 PASS EPISODE ID FOR FINAL STORAGE
        context["episode_id"] = episode["episode_id"]
        context["retrieved"] = top
        context["past_memory"] = [episode]

        print("[DEBUG][MEMORY] Episode updated →", episode["episode_id"])
        return context
