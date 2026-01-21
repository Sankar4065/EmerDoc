import uuid
from qdrant_client.models import VectorParams, Distance, PointStruct
from intent.embedder import embed
from memory.qdrant_client import client

LONG_TERM_COLLECTION = "long_term_memory"


def init_long_term_collection():
    collections = client.get_collections().collections
    names = [c.name for c in collections]

    if LONG_TERM_COLLECTION not in names:
        client.create_collection(
            collection_name=LONG_TERM_COLLECTION,
            vectors_config=VectorParams(
                size=384,
                distance=Distance.COSINE
            )
        )


def store_long_term_memory(text: str, category: str = "general"):
    vector = embed(text)

    point = PointStruct(
        id=str(uuid.uuid4()),
        vector=vector,
        payload={
            "type": "long_term",
            "category": category,
            "text": text
        }
    )

    client.upsert(
        collection_name=LONG_TERM_COLLECTION,
        points=[point]
    )


def retrieve_long_term_memory(query: str, limit: int = 3):
    query_vector = embed(query)

    results = client.query_points(
        collection_name=LONG_TERM_COLLECTION,
        query=query_vector,
        limit=limit,
        with_payload=True
    )

    memories = []

    for r in results.points:
        if r.payload.get("type") == "long_term":
            memories.append(r.payload["text"])

    return memories
