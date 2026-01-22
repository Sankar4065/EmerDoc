from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image
import torch

processor = BlipProcessor.from_pretrained(
    "Salesforce/blip-image-captioning-base"
)

model = BlipForConditionalGeneration.from_pretrained(
    "Salesforce/blip-image-captioning-base"
)

model.eval()

def image_to_text(image_path: str) -> str:
    image = Image.open(image_path).convert("RGB")

    inputs = processor(
        images=image,
        return_tensors="pt"
    )

    with torch.no_grad():
        output = model.generate(
            **inputs,
            max_new_tokens=40
        )

    caption = processor.decode(output[0], skip_special_tokens=True)
    return caption
