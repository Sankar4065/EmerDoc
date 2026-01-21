import os
from groq import Groq

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

KNOWLEDGE_PROMPT = """
Generate general medical first-aid information about the following keywords.

Rules:
- Do NOT diagnose
- Do NOT mention diseases
- Keep it generic and educational
- Generate max 25 points
- Each point max 30 words
- No personalization

Keywords:
{keywords}
"""

def generate_knowledge(keywords: list[str]) -> str:
    keyword_text = ", ".join(keywords)

    prompt = KNOWLEDGE_PROMPT.format(keywords=keyword_text)

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "You are a medical first-aid information assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2,
        max_tokens=700
    )

    return response.choices[0].message.content.strip()

