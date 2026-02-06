import uuid
from datetime import datetime
from collections import defaultdict

from qdrant_client.models import VectorParams, Distance, PointStruct
from intent.embedder import embed
from memory.qdrant_client import client


# ======================================================
# COLLECTION CONFIG
# ======================================================

PERSONAL_MEMORY_COLLECTION = "personal_memory"


# ======================================================
# 1️⃣ INIT COLLECTION
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
        print("[DEBUG][PERSONAL][INIT] Personal memory collection created")
    else:
        print("[DEBUG][PERSONAL][INIT] Personal memory collection already exists")


# ======================================================
# 2️⃣ DELETE EXISTING RECORD (OVERWRITE RULE)
# ======================================================

def delete_existing_personal_record(
    name: str,
    issue: str,
    date: str
):
    results, _ = client.scroll(
        collection_name=PERSONAL_MEMORY_COLLECTION,
        with_payload=True,
        limit=50
    )

    ids_to_delete = []

    for r in results:
        payload = r.payload or {}

        if (
            payload.get("type") == "personal"
            and payload.get("name") == name
            and payload.get("issue") == issue
            and payload.get("date") == date
        ):
            ids_to_delete.append(r.id)

    if ids_to_delete:
        client.delete(
            collection_name=PERSONAL_MEMORY_COLLECTION,
            points_selector=ids_to_delete
        )
        print(
            f"[DEBUG][PERSONAL] Removed {len(ids_to_delete)} old record(s) "
            f"for {name} / {issue} / {date}"
        )


# ======================================================
# 3️⃣ STORE PERSONAL MEDICAL DATA
# ======================================================

def store_personal_medical_data(
    name: str,
    symptoms: list[str],
    cause: str,
    issue: str,
    care_suggestions: list[str],
    date: str | None = None
):
    if not date:
        date = datetime.utcnow().date().isoformat()

    # 🔒 Overwrite rule
    delete_existing_personal_record(name, issue, date)

    symptoms_text = ", ".join(symptoms)
    care_text = ", ".join(care_suggestions)

    semantic_text = (
        f"Patient {name} experienced symptoms {symptoms_text}. "
        f"Issue identified as {issue}. "
        f"Care suggestions: {care_text}."
    )

    vector = embed(semantic_text)

    point = PointStruct(
        id=str(uuid.uuid4()),
        vector=vector,
        payload={
            "type": "personal",
            "name": name,
            "date": date,
            "symptoms": symptoms,
            "cause": cause,
            "issue": issue,
            "care_suggestions": care_suggestions
        }
    )

    client.upsert(
        collection_name=PERSONAL_MEMORY_COLLECTION,
        points=[point]
    )

    print(
        f"[DEBUG][PERSONAL] Stored personal record → "
        f"name={name}, issue={issue}, symptoms={symptoms}"
    )


# ======================================================
# 4️⃣ SIMILARITY → WEIGHT MAPPING
# ======================================================

def similarity_to_weight(similarity: float) -> float:
    if similarity >= 0.90:
        return 1.0
    elif similarity >= 0.85:
        return 0.9
    elif similarity >= 0.80:
        return 0.8
    elif similarity >= 0.75:
        return 0.7
    elif similarity >= 0.70:
        return 0.6
    else:
        return 0.0


# ======================================================
# 5️⃣ RETRIEVE SIMILAR PERSONAL RECORDS
# ======================================================

def retrieve_similar_personal_records(
    symptoms: list[str],
    limit: int = 20
):
    symptoms_text = ", ".join(symptoms)
    query_text = f"Patient experienced symptoms {symptoms_text}."

    query_vector = embed(query_text)

    results = client.query_points(
        collection_name=PERSONAL_MEMORY_COLLECTION,
        query=query_vector,
        limit=limit,
        with_payload=True
    )

    return results.points


# ======================================================
# 6️⃣ ISSUE % DISTRIBUTION (SINGLE QUERY)
# ======================================================

def get_issue_percentages_from_personal_data(
    current_symptoms: list[str],
    limit: int = 20
):
    points = retrieve_similar_personal_records(
        symptoms=current_symptoms,
        limit=limit
    )

    issue_weights = defaultdict(float)

    for point in points:
        payload = point.payload or {}
        similarity = point.score

        if payload.get("type") != "personal":
            continue

        issue = payload.get("issue")
        if not issue:
            continue

        weight = similarity_to_weight(similarity)
        if weight == 0.0:
            continue

        issue_weights[issue] += weight

    total = sum(issue_weights.values())
    if total == 0:
        return {}

    return {
        issue: round((weight / total) * 100, 2)
        for issue, weight in issue_weights.items()
    }


# ======================================================
# 7️⃣ ISSUE % DISTRIBUTION (SYMPTOM-WISE AGGREGATION)
# ======================================================

def get_issue_percentages_from_symptoms(
    symptoms: list[str]
):
    aggregated = defaultdict(float)

    for symptom in symptoms:
        percentages = get_issue_percentages_from_personal_data(
            current_symptoms=[symptom]
        )

        for issue, pct in percentages.items():
            aggregated[issue] += pct

    total = sum(aggregated.values())
    if total == 0:
        return {}

    return {
        issue: round((value / total) * 100, 2)
        for issue, value in aggregated.items()
    }
