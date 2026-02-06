from agents.base import Agent
from memory.personal_data import store_final_personal_data

class ReasoningAgent(Agent):
    def run(self, context: dict) -> dict:
        print("Reasoning agent running...")

        user_id = context["user_id"]
        episode_id = context["episode_id"]
        symptoms = context.get("symptoms", [])
        issue = context.get("issue")
        care = context.get("retrieved", [])

        print("[DEBUG][REASONING] Final issue →", issue)

        store_final_personal_data(
            user_id=user_id,
            episode_id=episode_id,
            symptoms=symptoms,
            issue=issue,
            care_suggestions=care
        )

        return {
            "answer": care,
            "issue": issue,
            "episode_id": episode_id,
            "source": "episodic_reasoning"
        }
