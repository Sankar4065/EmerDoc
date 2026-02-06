from agents.base import Agent
from intent.intent_extractor import extract_intent

from knowledge.llm_generator import (
    extract_symptoms_from_intent,
    refine_issue_with_personal_data
)

from memory.personal_data import (
    get_issue_percentages_from_symptoms
)

class PlannerAgent(Agent):
    def run(self, context: dict, agents: dict) -> dict:
        print("Planner agent running...")

        while context["stage"] != 5:
            print(f"[DEBUG][PLANNER] Current stage → {context['stage']}")

            # -------------------------------------------------
            # STAGE 1: Intent + symptoms
            # -------------------------------------------------
            if context["stage"] == 1:
                intent = extract_intent(context["query"])
                context["intent"] = intent

                print("[DEBUG][PLANNER] Intent →", intent)

                symptoms = extract_symptoms_from_intent(intent)
                context["symptoms"] = symptoms

                print("[DEBUG][PLANNER] Symptoms →", symptoms)

                # 🔥 PERSONAL MEMORY LOOKUP
                issue_dist = get_issue_percentages_from_symptoms(symptoms)
                context["personal_issue_distribution"] = issue_dist

                print("[DEBUG][PLANNER] Personal issue % →", issue_dist)

                # 🔥 ISSUE REFINEMENT
                refined_issue = refine_issue_with_personal_data(
                    symptoms,
                    issue_dist
                )

                context["issue"] = refined_issue
                print("[DEBUG][PLANNER] Final issue →", refined_issue)

                context["stage"] = 2

            elif context["stage"] == 2:
                context = agents["knowledge"].run(context)
                context["stage"] = 3

            elif context["stage"] == 3:
                context = agents["critic"].run(context)
                context["stage"] = 4

            elif context["stage"] == 4:
                context = agents["memory"].run(context)
                context["stage"] = 5

        print("[DEBUG][PLANNER] Pipeline completed")
        return context
