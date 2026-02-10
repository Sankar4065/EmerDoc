from agents.base import Agent
from knowledge.llm_generator import generate_knowledge
from knowledge.point_parser import split_into_points


class KnowledgeAgent(Agent):
    def run(self, context: dict) -> dict:
        if context["stage"] != 2:
            return context

        print("Knowledge agent running...")

        issue = context.get("issue")
        symptoms = context.get("symptoms", [])

        raw = generate_knowledge(
            issue,
             symptoms,
             prior_safe_care=context.get("personal_safe_care", [])
             )

        if not raw or not raw.strip():
            context["raw_points"] = []
            return context

        # 🔒 HARD SANITIZATION
        raw = raw.replace("•", "\n")
        raw = raw.replace(";", "\n")
        raw = raw.replace("—", "\n")
        raw = raw.replace(" - ", "\n")

        # 🔒 Sentence fallback split
        raw = raw.replace(". ", ".\n")

        raw = raw.strip()

        print("[DEBUG][KNOWLEDGE] Sanitized raw ↓")
        print(raw)

        points = split_into_points(raw)

        print(f"[DEBUG][KNOWLEDGE] Final points → {len(points)}")
        for p in points:
            print("  →", p)

        context["raw_points"] = points
        return context
