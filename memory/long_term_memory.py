import uuid
from datetime import datetime, timedelta

from qdrant_client.models import VectorParams, Distance, PointStruct

from intent.embedder import embed
from memory.qdrant_client import client


# ======================================================
# COLLECTION CONFIG
# ======================================================

LONG_TERM_COLLECTION = "long_term_memory"


# ======================================================
# INIT (USED BY app.py STARTUP)
# ======================================================

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
        print("[DEBUG][INIT] Long-term episodic collection created")
    else:
        print("[DEBUG][INIT] Long-term episodic collection already exists")


# ======================================================
# EPISODE CREATION
# ======================================================

def create_episode(user_id: str) -> dict:
    start = datetime.utcnow()
    end = start + timedelta(hours=24)

    episode = {
        "episode_id": str(uuid.uuid4()),
        "user_id": user_id,

        "episode_start": start.isoformat(),
        "episode_end": end.isoformat(),

        "symptoms": [],
        "cause": None,
        "issue": None,

        "care_suggestions": [],
        "source": "episodic_chat"
    }

    print(f"[DEBUG][EPISODE] Created new episode → {episode['episode_id']}")
    print(f"[DEBUG][EPISODE] Start → {episode['episode_start']}")
    print(f"[DEBUG][EPISODE] End   → {episode['episode_end']}")

    return episode


# ======================================================
# STORE / UPSERT EPISODE
# ======================================================

def store_episode(episode: dict):
    print(f"[DEBUG][EPISODE] Storing episode → {episode['episode_id']}")
    print(f"[DEBUG][EPISODE] Care suggestions count → {len(episode['care_suggestions'])}")

    # Vector uses ONLY safe abstractions
    text_for_embedding = " ".join(episode["care_suggestions"])

    if not text_for_embedding:
        text_for_embedding = episode["user_id"]

    vector = embed(text_for_embedding)

    point = PointStruct(
        id=episode["episode_id"],
        vector=vector,
        payload={
            "type": "episodic",
            "episode": episode
        }
    )

    client.upsert(
        collection_name=LONG_TERM_COLLECTION,
        points=[point]
    )

    print("[DEBUG][EPISODE] Episode stored in Qdrant")


# ======================================================
# RETRIEVE LATEST EPISODE FOR USER
# ======================================================

def retrieve_latest_episode(user_id: str):
    results, _ = client.scroll(
        collection_name=LONG_TERM_COLLECTION,
        with_payload=True,
        limit=20
    )

    episodes = []

    for r in results:
        payload = r.payload or {}

        if payload.get("type") != "episodic":
            continue

        episode = payload.get("episode")
        if not episode:
            continue

        if episode.get("user_id") == user_id:
            episodes.append(episode)

    if not episodes:
        print("[DEBUG][EPISODE] No existing episode found")
        return None

    episodes.sort(
        key=lambda e: e["episode_start"],
        reverse=True
    )

    latest = episodes[0]
    print(f"[DEBUG][EPISODE] Retrieved latest episode → {latest['episode_id']}")

    return latest
