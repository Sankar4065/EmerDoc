import whisper

model = whisper.load_model("small")

def audio_to_text(audio_path: str) -> str:
    result = model.transcribe(audio_path)
    return result["text"]
