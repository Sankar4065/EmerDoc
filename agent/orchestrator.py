from agents.planner_agent import PlannerAgent
from agents.knowledge_agent import KnowledgeAgent
from agents.critic_agent import CriticAgent
from agents.memory_agent import MemoryAgent
from agents.reasoning_agent import ReasoningAgent

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

        "stage": 1
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
