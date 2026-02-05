from agents.base import Agent
from knowledge.safety import (
    normalize_point,
    is_action_point,
    is_safe_first_aid
)
from knowledge.knowledge_limiter import limit_knowledge

class CriticAgent(Agent):
    def run(self, context: dict) -> dict:
        if context["stage"] != 3:
            return context

        print("Critic agent running...")
        safe_points = []

        for p in context["raw_points"]:
            clean = normalize_point(p)
            print(f"[DEBUG][CRITIC] Normalized → {clean}")

            if is_action_point(clean) and is_safe_first_aid(clean):
                limited = limit_knowledge(clean)
                safe_points.append(limited)
                print("  ✅ Approved:", limited)
            else:
                print("  ❌ Rejected:", clean)

        context["validated_points"] = safe_points
        print(f"[DEBUG][CRITIC] Valid points → {len(safe_points)}")
        return context
