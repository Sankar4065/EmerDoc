from agents.base import Agent
from intent.intent_extractor import extract_intent
from knowledge.llm_generator import (
    extract_symptoms_from_intent,
    refine_issue_with_personal_data,
    normalize_issue
)
from memory.personal_data import get_issue_percentages_from_symptoms
from knowledge.severity import should_escalate_issue


class PlannerAgent(Agent):
    def run(self, context: dict, agents: dict) -> dict:
        print("Planner agent running...")

        # ==================================================
        # HYDRATE PREVIOUS ISSUE (CRITICAL FOR ESCALATION)
        # ==================================================
        # Use last episode issue if current issue is None
        previous_episode_issue = context.get("last_episode_issue")
        if context.get("issue") is None and previous_episode_issue:
            context["issue"] = previous_episode_issue
            print(f"[DEBUG][PLANNER] Loaded previous issue → {previous_episode_issue}")

        while context["stage"] != 5:
            print(f"[DEBUG][PLANNER] Current stage → {context['stage']}")

            # ==================================================
            # STAGE 1 — INTENT → SYMPTOMS → ISSUE DECISION
            # ==================================================
            if context["stage"] == 1:
                # -------- Intent --------
                intent = extract_intent(context["query"])
                context["intent"] = intent
                print("[DEBUG][PLANNER] Intent →", intent)

                # -------- Symptoms --------
                symptoms = extract_symptoms_from_intent(intent)
                context["symptoms"] = symptoms
                print("[DEBUG][PLANNER] Symptoms →", symptoms)

                # -------- Personal priors --------
                issue_dist = get_issue_percentages_from_symptoms(symptoms)
                context["personal_issue_distribution"] = issue_dist
                print("[DEBUG][PLANNER] Personal issue % →", issue_dist)

                # -------- Issue refinement --------
                refined_issue = refine_issue_with_personal_data(
                    symptoms, issue_dist
                )

                refined_issue = normalize_issue(refined_issue)
                previous_issue = context.get("issue")

                # -------- Severity escalation guard --------
                if refined_issue != "unknown":
                    if should_escalate_issue(
                        previous_issue,
                        refined_issue,
                        symptoms
                    ):
                        context["issue"] = refined_issue
                    else:
                        print(
                            f"[DEBUG][PLANNER] Escalation blocked: "
                            f"{previous_issue} → {refined_issue}"
                        )
                        context["issue"] = previous_issue
                elif previous_issue is None:
                    context["issue"] = "unknown"

                print("[DEBUG][PLANNER] Final issue →", context["issue"])

                context["stage"] = 2

            # ==================================================
            # STAGE 2 — KNOWLEDGE GENERATION
            # ==================================================
            elif context["stage"] == 2:
                context = agents["knowledge"].run(context)
                context["stage"] = 3

            # ==================================================
            # STAGE 3 — SAFETY / CRITIC
            # ==================================================
            elif context["stage"] == 3:
                context = agents["critic"].run(context)
                context["stage"] = 4

            # ==================================================
            # STAGE 4 — MEMORY
            # ==================================================
            elif context["stage"] == 4:
                context = agents["memory"].run(context)
                context["stage"] = 5

        print("[DEBUG][PLANNER] Pipeline completed")
        return context
