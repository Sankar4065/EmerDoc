from agents.planner_agent import PlannerAgent
from agents.knowledge_agent import KnowledgeAgent
from agents.critic_agent import CriticAgent
from agents.memory_agent import MemoryAgent
from agents.reasoning_agent import ReasoningAgent

from memory.temp_memory import init_collection
from memory.long_term_memory import init_long_term_collection


def run_agent(query: str, user_id: str):
    # # 🔹 INIT MEMORY ONCE
    # print("[INIT] Initializing Qdrant collections...")
    # init_collection()
    # init_long_term_collection()
    # print("[INIT] Qdrant ready")

    context = {
        "query": query,
        "user_id": user_id,
        "stage": 1,
        "raw_points": [],
        "validated_points": [],
        "retrieved": []
    }

    agents = {
        "knowledge": KnowledgeAgent(),
        "critic": CriticAgent(),
        "memory": MemoryAgent()
    }

    planner = PlannerAgent()
    context = planner.run(context, agents)

    reasoning = ReasoningAgent()
    return reasoning.run(context)
