import uuid
from collections import defaultdict
from qdrant_client.models import VectorParams, Distance, PointStruct
from intent.embedder import embed
from memory.qdrant_client import client

PERSONAL_MEMORY_COLLECTION = "personal_memory"


# ======================================================
# INIT
# ======================================================

def init_personal_memory_collection():
    collections = client.get_collections().collections
    names = [c.name for c in collections]

    if PERSONAL_MEMORY_COLLECTION not in names:
        client.create_collection(
            collection_name=PERSONAL_MEMORY_COLLECTION,
            vectors_config=VectorParams(
                size=384,
                distance=Distance.COSINE
            )
        )
        print("[DEBUG][PERSONAL][INIT] Collection created")
    else:
        print("[DEBUG][PERSONAL][INIT] Collection exists")


# ======================================================
# DELETE BY EPISODE (OVERWRITE RULE)
# ======================================================

def delete_episode_personal_record(user_id: str, episode_id: str):
    points, _ = client.scroll(
        collection_name=PERSONAL_MEMORY_COLLECTION,
        with_payload=True,
        limit=50
    )

    ids = [
        p.id for p in points
        if p.payload
        and p.payload.get("user_id") == user_id
        and p.payload.get("episode_id") == episode_id
    ]

    if ids:
        client.delete(
            collection_name=PERSONAL_MEMORY_COLLECTION,
            points_selector=ids
        )
        print(f"[DEBUG][PERSONAL] Overwritten old record for episode {episode_id}")


# ======================================================
# STORE FINAL PERSONAL DATA
# ======================================================

def store_final_personal_data(
    user_id: str,
    episode_id: str,
    symptoms: list[str],
    issue: str,
    care_suggestions: list[str]
):
    delete_episode_personal_record(user_id, episode_id)

    text = (
        f"User {user_id} episode {episode_id}. "
        f"Symptoms: {', '.join(symptoms)}. "
        f"Final issue: {issue}. "
        f"Care: {', '.join(care_suggestions)}."
    )

    vector = embed(text)

    point = PointStruct(
        id=str(uuid.uuid4()),
        vector=vector,
        payload={
            "type": "personal",
            "user_id": user_id,
            "episode_id": episode_id,
            "symptoms": symptoms,
            "issue": issue,
            "care_suggestions": care_suggestions
        }
    )

    client.upsert(
        collection_name=PERSONAL_MEMORY_COLLECTION,
        points=[point]
    )

    print(
        "[DEBUG][PERSONAL] Stored FINAL personal record → "
        f"user={user_id}, episode={episode_id}, issue={issue}"
    )


# ======================================================
# ISSUE % FROM PERSONAL DATA (UNCHANGED)
# ======================================================

def similarity_to_weight(score: float) -> float:
    if score >= 0.9: return 1.0
    if score >= 0.8: return 0.8
    if score >= 0.7: return 0.6
    return 0.0


def get_issue_percentages_from_symptoms(symptoms: list[str]):
    if not symptoms:
        return {}

    vector = embed(" ".join(symptoms))

    results = client.query_points(
        collection_name=PERSONAL_MEMORY_COLLECTION,
        query=vector,
        limit=20,
        with_payload=True
    )

    weights = defaultdict(float)

    for p in results.points:
        issue = p.payload.get("issue")
        w = similarity_to_weight(p.score)
        if issue and w:
            weights[issue] += w

    total = sum(weights.values())
    if total == 0:
        return {}

    return {k: round(v / total * 100, 2) for k, v in weights.items()}
