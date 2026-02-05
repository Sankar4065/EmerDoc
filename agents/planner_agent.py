from agents.base import Agent
from intent.intent_extractor import extract_intent

class PlannerAgent(Agent):
    def run(self, context: dict, agents: dict) -> dict:
        print("Planner agent running...")

        while context["stage"] != 5:
            print(f"[DEBUG][PLANNER] Current stage → {context['stage']}")

            # 🟢 STAGE 1: Understand intent
            if context["stage"] == 1:
                query = context["query"]
                intent = extract_intent(query)

                context["intent"] = intent
                context["should_retrieve"] = len(intent) > 0

                print(f"[DEBUG][PLANNER] Intent detected → {intent}")
                context["stage"] = 2

            # 🟢 STAGE 2: Knowledge generation
            elif context["stage"] == 2:
                context = agents["knowledge"].run(context)
                context["stage"] = 3

            # 🟢 STAGE 3: Critic / validation
            elif context["stage"] == 3:
                context = agents["critic"].run(context)
                context["stage"] = 4

            # 🟢 STAGE 4: Memory store & retrieve
            elif context["stage"] == 4:
                context = agents["memory"].run(context)
                context["stage"] = 5

        print("[DEBUG][PLANNER] Pipeline completed")
        return context
