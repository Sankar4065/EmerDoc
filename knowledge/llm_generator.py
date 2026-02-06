import os
from groq import Groq

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# -------------------------------------------------
# KNOWLEDGE GENERATION (unchanged)
# -------------------------------------------------

KNOWLEDGE_PROMPT = """
Generate general medical first-aid guidance.

Context:
- Health issue: {issue}
- Symptoms: {symptoms}

Rules:
- Do NOT diagnose
- Do NOT mention diseases
- Educational only
- Max 25 points
- Each point max 30 words
- Action-oriented
"""

def generate_knowledge(issue: str, symptoms: list[str]) -> str:
    symptoms_text = ", ".join(symptoms) if symptoms else "none"

    print("[DEBUG][LLM] Generating knowledge")
    print("[DEBUG][LLM] Issue →", issue)
    print("[DEBUG][LLM] Symptoms →", symptoms_text)

    prompt = KNOWLEDGE_PROMPT.format(
        issue=issue or "unknown",
        symptoms=symptoms_text
    )

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "You are a medical first-aid assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2,
        max_tokens=700
    )

    return response.choices[0].message.content.strip()


# -------------------------------------------------
# SYMPTOM EXTRACTION (unchanged)
# -------------------------------------------------

SYMPTOM_EXTRACTION_PROMPT = """
Extract possible SYMPTOMS.

Rules:
- Single words only
- Comma-separated
- No explanations
- If none: none

Intent keywords:
{keywords}
"""

def extract_symptoms_from_intent(intent: list[str]) -> list[str]:
    if not intent:
        return []

    print("[DEBUG][LLM] Extracting symptoms from →", intent)

    prompt = SYMPTOM_EXTRACTION_PROMPT.format(
        keywords=", ".join(intent)
    )

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "You extract symptoms only."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.1,
        max_tokens=50
    )

    raw = response.choices[0].message.content.strip().lower()
    print("[DEBUG][LLM] Raw symptoms →", raw)

    if raw == "none":
        return []

    return [s.strip() for s in raw.split(",") if s.strip()]


# -------------------------------------------------
# 🔥 NEW: ISSUE REFINEMENT USING PERSONAL PRIORS
# -------------------------------------------------

ISSUE_REFINEMENT_PROMPT = """
Given symptoms and historical issue likelihoods,
return the MOST LIKELY general health issue.

Rules:
- Output ONE word only
- No explanation
- If unclear → unknown

Symptoms:
{symptoms}

Historical issue likelihoods:
{priors}
"""

def refine_issue_with_personal_data(
    symptoms: list[str],
    issue_percentages: dict
) -> str:

    priors_text = ", ".join(
        f"{k} ({v}%)" for k, v in issue_percentages.items()
    ) if issue_percentages else "none"

    print("[DEBUG][LLM] Refining issue")
    print("[DEBUG][LLM] Symptoms →", symptoms)
    print("[DEBUG][LLM] Priors →", priors_text)

    prompt = ISSUE_REFINEMENT_PROMPT.format(
        symptoms=", ".join(symptoms),
        priors=priors_text
    )

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "You infer general health issues only."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.1,
        max_tokens=20
    )

    issue = response.choices[0].message.content.strip().lower()
    issue = issue.split()[0]

    print("[DEBUG][LLM] Final refined issue →", issue)

    return issue if issue.isalpha() else "unknown"
