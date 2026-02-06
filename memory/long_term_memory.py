import uuid
from datetime import datetime, timedelta
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
            vectors_config=VectorParams(size=384, distance=Distance.COSINE)
        )
        print("[DEBUG][INIT] Long-term episodic collection created")


def create_episode(user_id: str) -> dict:
    start = datetime.utcnow()
    end = start + timedelta(hours=24)

    episode = {
        "episode_id": str(uuid.uuid4()),
        "user_id": user_id,
        "episode_start": start.isoformat(),
        "episode_end": end.isoformat(),
        "symptoms": [],
        "issues": [],
        "care_suggestions": [],
        "source": "episodic_chat"
    }

    print("[DEBUG][EPISODE] Created new episode →", episode["episode_id"])
    return episode


def store_episode(episode: dict):
    vector = embed(" ".join(episode["care_suggestions"]) or episode["user_id"])

    point = PointStruct(
        id=episode["episode_id"],
        vector=vector,
        payload={"type": "episodic", "episode": episode}
    )

    client.upsert(collection_name=LONG_TERM_COLLECTION, points=[point])

    print(
        f"[DEBUG][EPISODE] Stored episode → {episode['episode_id']} | "
        f"Symptoms={len(episode['symptoms'])} | Issues={len(episode['issues'])}"
    )


def retrieve_latest_episode(user_id: str):
    results, _ = client.scroll(
        collection_name=LONG_TERM_COLLECTION,
        with_payload=True,
        limit=20
    )

    episodes = [
        r.payload["episode"]
        for r in results
        if r.payload
        and r.payload.get("type") == "episodic"
        and r.payload["episode"]["user_id"] == user_id
    ]

    if not episodes:
        return None

    episodes.sort(key=lambda e: e["episode_start"], reverse=True)
    return episodes[0]
