from agents.base import Agent
from memory.long_term_memory import store_episode
from memory.personal_data import store_final_personal_data


class ReasoningAgent(Agent):
    def run(self, context: dict) -> dict:
        print("Reasoning agent running...")

        episode = context["episode"]

        user_id = context["user_id"]
        episode_id = episode["episode_id"]

        symptoms = context.get("symptoms", [])
        issue = context.get("issue")
        care = context.get("retrieved", [])

        # ==================================================
        # EPISODIC MEMORY (MERGE, NOT OVERWRITE)
        # ==================================================
        previous_symptoms = episode.get("symptoms", [])
        previous_care = episode.get("care_suggestions", [])

        episode["symptoms"] = list(set(previous_symptoms + symptoms))
        episode["issues"] = [issue] if issue else episode.get("issues", [])
        episode["care_suggestions"] = list(
            set(previous_care + care)
        )

        store_episode(episode)

        # ==================================================
        # PERSONAL MEMORY (DELETE → REPLACE)
        # ==================================================
        store_final_personal_data(
            user_id=user_id,
            episode_id=episode_id,
            symptoms=episode["symptoms"],
            issue=issue,
            care_suggestions=episode["care_suggestions"]
        )

        # ==================================================
        # WHY EXPLANATION
        # ==================================================
        why_parts = []

        if symptoms:
            why_parts.append(
                f"Based on your reported symptoms ({', '.join(symptoms)})"
            )
        else:
            why_parts.append("Based on limited symptom information")

        if context.get("last_episode_issue"):
            why_parts.append("and recent similar episodes")

        if context.get("escalation_blocked"):
            why_parts.append(
                "Serious conditions were considered but not supported by symptoms"
            )

        why_text = ". ".join(why_parts) + "."

        # ==================================================
        # 🧾 AUTO-GENERATED EPISODE SUMMARY (FULL EPISODE)
        # ==================================================
        summary_lines = []

        if episode["symptoms"]:
            summary_lines.append(
                f"Symptoms reported: {', '.join(episode['symptoms'])}"
            )
        else:
            summary_lines.append("Symptoms reported: none")

        if episode.get("issues"):
            summary_lines.append(
                f"Final issue considered: {episode['issues'][-1]}"
            )
        else:
            summary_lines.append("Final issue considered: unknown")

        if episode["care_suggestions"]:
            summary_lines.append(
                f"Care guidance given: {', '.join(episode['care_suggestions'])}"
            )
        else:
            summary_lines.append("Care guidance given: none")

        episode_summary = " | ".join(summary_lines)

        print(f"[DEBUG][REASONING] EPISODE SUMMARY → {episode_summary}")

        print(
            f"[DEBUG][REASONING] FINALIZED → episode={episode_id} | "
            f"issue={issue} | symptoms={len(episode['symptoms'])}"
        )

        return {
            "answer": episode["care_suggestions"],
            "final_issue": issue,
            "final_symptoms": episode["symptoms"],
            "episode_id": episode_id,
            "why": why_text,
            "episode_summary": episode_summary,
            "source": "episodic_reasoned"
        }
