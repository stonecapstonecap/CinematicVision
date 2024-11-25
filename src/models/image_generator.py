from diffusers import StableDiffusionPipeline
from src.config import MODEL_PATH

text_to_image = StableDiffusionPipeline.from_pretrained(MODEL_PATH, device_map="balanced")

def generate_image(description):
    return text_to_image(description).images[0]

def regenerate_image(description, additional_prompt):
    refined_description = f"{description}. {additional_prompt}"
    return generate_image(refined_description)
