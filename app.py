from fastapi import FastAPI, UploadFile, File, Form
import shutil
import os

# 🔹 Agent pipeline
from agent.orchestrator import run_agent

# 🔹 Modality router
from modality.modality_router import normalize_input

# 🔹 Memory layers (INFRA)
from memory.temp_memory import init_collection
from memory.long_term_memory import init_long_term_collection
from memory.personal_data import init_personal_memory_collection


app = FastAPI()


# ======================================================
# 🔹 STARTUP: Initialize ALL memory layers
# ======================================================
@app.on_event("startup")
def startup_event():
    print("[STARTUP] Initializing Qdrant collections...")

    init_collection()                     # Short-term (TTL)
    init_long_term_collection()           # Episodic memory
    init_personal_memory_collection()     # Personal medical memory

    print("[STARTUP] Qdrant ready")


# ======================================================
# 🔹 Health check
# ======================================================
@app.get("/")
def health():
    return {"status": "EmerDoc Privacy Agent running"}


# ======================================================
# 🔹 Main API endpoint
# ======================================================
@app.post("/ask")
def ask(
    query: str | None = Form(None),
    user_id: str = Form("demo_user"),
    image: UploadFile | None = File(None),
    audio: UploadFile | None = File(None)
):
    image_path = None
    audio_path = None

    # --------------------------------------------------
    # 🔹 Save image temporarily
    # --------------------------------------------------
    if image:
        image_path = f"temp_{image.filename}"
        with open(image_path, "wb") as f:
            shutil.copyfileobj(image.file, f)
        print(f"[DEBUG][APP] Image saved → {image_path}")

    # --------------------------------------------------
    # 🔹 Save audio temporarily
    # --------------------------------------------------
    if audio:
        audio_path = f"temp_{audio.filename}"
        with open(audio_path, "wb") as f:
            shutil.copyfileobj(audio.file, f)
        print(f"[DEBUG][APP] Audio saved → {audio_path}")

    try:
        # --------------------------------------------------
        # 🔹 Normalize multimodal input → TEXT
        # --------------------------------------------------
        normalized_text = normalize_input(
            text=query,
            image_path=image_path,
            audio_path=audio_path
        )

        print(f"[DEBUG][APP] Normalized input → {normalized_text}")

        # --------------------------------------------------
        # 🔹 Run MULTI-AGENT pipeline
        # --------------------------------------------------
        response = run_agent(
            query=normalized_text,
            user_id=user_id
        )

    finally:
        # --------------------------------------------------
        # 🔒 Privacy cleanup
        # --------------------------------------------------
        if image_path and os.path.exists(image_path):
            os.remove(image_path)
            print(f"[DEBUG][APP] Removed temp image → {image_path}")

        if audio_path and os.path.exists(audio_path):
            os.remove(audio_path)
            print(f"[DEBUG][APP] Removed temp audio → {audio_path}")

    return response
