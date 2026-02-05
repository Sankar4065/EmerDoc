from agents.base import Agent
from knowledge.llm_generator import generate_knowledge
from knowledge.point_parser import split_into_points

class KnowledgeAgent(Agent):
    def run(self, context: dict) -> dict:
        if context["stage"] != 2:
            return context

        print("Knowledge agent running...")
        intent = context["intent"]

        raw = generate_knowledge(intent)
        points = split_into_points(raw)

        print(f"[DEBUG][KNOWLEDGE] Raw points generated → {len(points)}")
        for p in points:
            print("  →", p)

        context["raw_points"] = points
        return context
