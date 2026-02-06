from agents.planner_agent import PlannerAgent
from agents.knowledge_agent import KnowledgeAgent
from agents.critic_agent import CriticAgent
from agents.memory_agent import MemoryAgent
from agents.reasoning_agent import ReasoningAgent

# 🔥 ADD THIS IMPORT
from memory.long_term_memory import retrieve_latest_episode


def run_agent(query: str, user_id: str):
    context = {
        "query": query,
        "user_id": user_id,

        "intent": [],
        "symptoms": [],
        "issue": None,

        "raw_points": [],
        "validated_points": [],
        "retrieved": [],

        # 🔥 NEW: preload slot (safe default)
        "last_episode_issue": None,

        "stage": 1
    }

    # ==================================================
    # 🔥 PRELOAD LAST EPISODE ISSUE (CRITICAL FIX)
    # ==================================================
    last_episode = retrieve_latest_episode(user_id)
    if last_episode and last_episode.get("issues"):
        context["last_episode_issue"] = last_episode["issues"][-1]
        print(
            f"[DEBUG][ORCH] Preloaded last episode issue → "
            f"{context['last_episode_issue']}"
        )

    agents = {
        "knowledge": KnowledgeAgent(),
        "critic": CriticAgent(),
        "memory": MemoryAgent()
    }

    planner = PlannerAgent()
    context = planner.run(context, agents)

    reasoning = ReasoningAgent()
    return reasoning.run(context)
