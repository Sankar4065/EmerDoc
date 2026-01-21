from qdrant_client import QdrantClient

# Local Qdrant (Docker)
client = QdrantClient(
    host="localhost",
    port=6333
)

COLLECTION_NAME = "temp_knowledge"
