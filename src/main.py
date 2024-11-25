from src.utils.pdf_processor import process_pdf
from src.models.image_generator import generate_image

def generate_images_from_pdf(pdf_path):
    scene_details = process_pdf(pdf_path)
    if not scene_details:
        return "No scene details found.", [], []
    
    locations = []
    images = []
    elaborative_descriptions = scene_details.get("elaborative_descriptions", {})
    scene_tips = scene_details.get("scene_improvement_tips", {})
    tips_text = "\n".join([f"{key}: {value}" for key, value in scene_tips.items()])

    for description in elaborative_descriptions.values():
        image = generate_image(description)
        locations.append(description)
        images.append(image)

    return "\n".join(locations), tips_text, images
