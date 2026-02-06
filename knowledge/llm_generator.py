import os
import re
from groq import Groq

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# -------------------------------------------------
# KNOWLEDGE GENERATION
# -------------------------------------------------

KNOWLEDGE_PROMPT = """
Generate output based on the given context.

Context:
- Health issue: {issue}
- Symptoms: {symptoms}

STRICT RULES:
- Do NOT diagnose
- Do NOT mention diseases
- Do NOT mention medical conditions by name
- Do NOT give explanations
- Educational only
- Action-oriented
- Max 25 points
- Each point max 30 words

CRITICAL FALLBACK RULE:
- If symptoms are "none"
  OR symptoms are empty
  OR symptoms are clearly NOT medical
  OR context is unclear

THEN:
- Output EXACTLY ONE single-line statement
- That line must be NON-MEDICAL
- That line must be a neutral guidance or clarification
- No bullets, no numbering, no formatting

NORMAL CASE:
- If valid medical symptoms exist:
  - Return first-aid guidance points
  - Each point must be a single actionable sentence

OUTPUT FORMAT:
- Either:
  • multiple action-oriented points
- OR:
  • exactly ONE plain sentence (fallback case)

NO extra text.
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
# SYMPTOM EXTRACTION
# -------------------------------------------------

SYMPTOM_EXTRACTION_PROMPT = """
Extract SYMPTOMS from intent keywords.

STRICT OUTPUT RULES:
- Output ONLY symptom words
- Comma-separated
- NO explanations
- NO extra text
- NO punctuation except commas
- If no symptom can be identified → output exactly: none

LANGUAGE RULES:
- Use simple, common words normal people use
- Avoid medical jargon
- Avoid partial or broken words

SYNONYM NORMALIZATION:
- dizzy / giddy / faint → dizziness
- cold / runny nose / sneezing → cold
- headache / head pain → headache
- loose motion / watery stool → diarrhea
- chest tight / short breath → breathlessness
- body ache / muscle pain → body pain

LOGIC:
1. If a keyword itself is a symptom → return it (normalized)
2. Merge similar keywords into one symptom
3. If no symptom is found:
   - Infer the TOP 1 most common symptom from the implied issue
4. If still unclear → output: none

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

    return [
    s.strip().strip(".")
    for s in raw.split(",")
    if s.strip()
]



# -------------------------------------------------
# 🔥 ISSUE REFINEMENT (FIXED)
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

    raw = response.choices[0].message.content.strip().lower()
    cleaned = re.sub(r"[^a-z]", "", raw)  # 🔥 FIX

    print("[DEBUG][LLM] Final refined issue →", cleaned or "unknown")

    return cleaned if cleaned else "unknown"


   # ===============================
# NORMALIZE ISSUE
# ===============================

def normalize_issue(issue: str) -> str:
    """
    Canonical normalization for common health issues.
    Deterministic, safe, and memory-stable.
    """

    if not issue:
        return issue

    text = issue.lower().strip()

    # ===============================
    # FEVER NORMALIZATION
    # ===============================
    fever_keywords = (
        "fever",
        "temperature",
        "feverish",
        "chills",
        "hot body",
        "raised temperature",
        "running temperature",
        "mild fever",
        "high fever"
    )

    if any(k in text for k in fever_keywords):
        return "fever"

    # ===============================
    # COUGH NORMALIZATION
    # ===============================
    cough_keywords = (
        "cough",
        "coughing",
        "dry cough",
        "wet cough",
        "productive cough",
        "persistent cough",
        "frequent cough",
        "chest cough",
        "throat cough",
        "night cough"
    )

    if any(k in text for k in cough_keywords):
        return "cough"

    # ===============================
    # COLD NORMALIZATION
    # ===============================
    cold_keywords = (
        "cold",
        "common cold",
        "head cold",
        "runny nose",
        "running nose",
        "blocked nose",
        "stuffy nose",
        "nasal congestion",
        "sneezing",
        "cold symptoms",
        "caught a cold"
    )

    if any(k in text for k in cold_keywords):
        return "commoncold"

    # ===============================
    # FALLBACK (DO NOT OVERREACH)
    # ===============================
    return issue
