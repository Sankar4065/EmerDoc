from modality.image_processor import image_to_text
from modality.audio_processor import audio_to_text

def normalize_input(
    text: str | None = None,
    image_path: str | None = None,
    audio_path: str | None = None
):
    if image_path:
        return image_to_text(image_path)

    if audio_path:
        return audio_to_text(audio_path)

    return text
