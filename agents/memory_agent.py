from agents.base import Agent
from memory.temp_memory import store_temp_knowledge, retrieve_temp_knowledge
from memory.long_term_memory import create_episode, retrieve_latest_episode
from memory.input_time_tracker import InputTimeTracker

time_tracker = InputTimeTracker()


class MemoryAgent(Agent):
    def run(self, context: dict) -> dict:
        if context["stage"] != 4:
            return context

        print("Memory agent running...")

        user_id = context["user_id"]
        validated = context.get("validated_points", [])

        # ==================================================
        # TEMP MEMORY (TTL-based)
        # ==================================================
        for p in validated:
            store_temp_knowledge(p)

        top = retrieve_temp_knowledge(context["query"], limit=3)
        print("[DEBUG][MEMORY] Retrieved temp →", top)

        # ==================================================
        # EPISODE FETCH (READ-ONLY)
        # ==================================================
        gap = time_tracker.check_time_gap()

        episode = (
            retrieve_latest_episode(user_id)
            if gap == "less_than_30_minutes"
            else None
        )

        if episode is None:
            episode = create_episode(user_id)

        # ❌ DO NOT MUTATE EPISODE HERE
        # ❌ DO NOT EXPOSE last_episode_issue HERE

        context["episode"] = episode
        context["retrieved"] = top

        print(
            f"[DEBUG][MEMORY] Episode fetched → {episode['episode_id']} | "
            f"Symptoms={len(episode['symptoms'])} | Issues={len(episode['issues'])}"
        )

        return context
