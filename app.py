from fastapi import FastAPI, UploadFile, File, Form
import shutil
import os

# ✅ IMPORTANT: use orchestrator, NOT agent.py
from agent.orchestrator import run_agent

from modality.modality_router import normalize_input
from memory.temp_memory import init_collection
from memory.long_term_memory import init_long_term_collection

app = FastAPI()


# 🔹 Run once when server starts
@app.on_event("startup")
def startup_event():
    print("[STARTUP] Initializing Qdrant collections...")
    init_collection()
    init_long_term_collection()
    print("[STARTUP] Qdrant ready")


@app.get("/")
def health():
    return {"status": "EmerDoc Privacy Agent running"}


@app.post("/ask")
def ask(
    query: str | None = Form(None),
    user_id: str = Form("demo_user"),
    image: UploadFile | None = File(None),
    audio: UploadFile | None = File(None)
):
    image_path = None
    audio_path = None

    # 🔹 Save image temporarily
    if image:
        image_path = f"temp_{image.filename}"
        with open(image_path, "wb") as f:
            shutil.copyfileobj(image.file, f)

    # 🔹 Save audio temporarily
    if audio:
        audio_path = f"temp_{audio.filename}"
        with open(audio_path, "wb") as f:
            shutil.copyfileobj(audio.file, f)

    try:
        # 🔹 Normalize multimodal input → TEXT
        normalized_text = normalize_input(
            text=query,
            image_path=image_path,
            audio_path=audio_path
        )

        # 🔹 Run MULTI-AGENT pipeline
        response = run_agent(
            query=normalized_text,
            user_id=user_id
        )

    finally:
        # 🔒 Privacy: cleanup temp files
        if image_path and os.path.exists(image_path):
            os.remove(image_path)
        if audio_path and os.path.exists(audio_path):
            os.remove(audio_path)

    return response
