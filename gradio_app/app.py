import gradio as gr
from src.main import generate_images_from_pdf
from src.models.image_generator import regenerate_image

def create_app():
    with gr.Blocks() as demo:
        gr.Markdown("## Scene Image Generator from PDF Script")

        with gr.Row():
            pdf_file = gr.File(file_types=[".pdf"], label="Upload PDF Script")
        generate_button = gr.Button("Generate Images")

        with gr.Row():
            location = gr.Textbox(label="Location Details")
            tips = gr.Textbox(label="Scene Improvement Tips")
            gallery = gr.Gallery(label="Generated Images")

        with gr.Row():
            additional_prompt = gr.Textbox(label="Additional Prompt for Refinement")
            regenerate_button = gr.Button("Regenerate Image")

        generate_button.click(generate_images_from_pdf, inputs=pdf_file, outputs=[location, tips, gallery])
        regenerate_button.click(regenerate_image, inputs=[location, additional_prompt], outputs=gallery)

        return demo

app = create_app()

if __name__ == "__main__":
    app.launch(share=True)
