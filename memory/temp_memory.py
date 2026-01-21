import uuid
from datetime import datetime, timedelta
from qdrant_client.models import VectorParams, Distance, PointStruct
from intent.embedder import embed
from memory.qdrant_client import client, COLLECTION_NAME

TTL_MINUTES = 0.2


def init_collection():
    collections = client.get_collections().collections
    names = [c.name for c in collections]

    if COLLECTION_NAME not in names:
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(
                size=384,
                distance=Distance.COSINE
            )
        )


def store_temp_knowledge(text: str):
    vector = embed(text)

    expires_at = (
        datetime.utcnow() + timedelta(minutes=TTL_MINUTES)
    ).isoformat()

    point = PointStruct(
        id=str(uuid.uuid4()),
        vector=vector,
        payload={
            "type": "temp",
            "kind": "first_aid_action",   # 🔥 METADATA
            "text": text,
            "expires_at": expires_at
        }
    )

    client.upsert(
        collection_name=COLLECTION_NAME,
        points=[point]
    )


def cleanup_expired_memory():
    now = datetime.utcnow()

    points, _ = client.scroll(
        collection_name=COLLECTION_NAME,
        with_payload=True,
        limit=100
    )

    expired_ids = []

    for point in points:
        payload = point.payload

        if payload.get("type") != "temp":
            continue

        if "expires_at" not in payload:
            continue

        expires_at = datetime.fromisoformat(payload["expires_at"])

        if now > expires_at:
            expired_ids.append(point.id)

    if expired_ids:
        client.delete(
            collection_name=COLLECTION_NAME,
            points_selector=expired_ids
        )


def retrieve_temp_knowledge(query: str, limit: int = 3):
    cleanup_expired_memory()

    query_vector = embed(query)

    results = client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_vector,
        limit=limit,
        with_payload=True
    )

    now = datetime.utcnow()
    valid_results = []

    for r in results.points:
        payload = r.payload

        if payload.get("type") != "temp":
            continue

        if payload.get("kind") != "first_aid_action":
            continue

        if "expires_at" not in payload:
            continue

        expires_at = datetime.fromisoformat(payload["expires_at"])

        if now <= expires_at:
            valid_results.append(payload["text"])

    return valid_results
