import gradio as gr
import json
from api_client import AxeraClient

def get_client(url):
    return AxeraClient(url)

def run_generate(url, mode, prompt, seed, init_image, strength, resize_mode):
    client = get_client(url)
    result = client.generate(
        mode=mode,
        prompt=prompt,
        seed=int(seed),
        init_image=init_image,
        denoising_strength=strength,
        resize_mode=int(resize_mode)
    )
    
    if "image" in result:
        metadata = {
            "Seed": result["seed"],
            "Total Time (ms)": result["total_time_ms"],
            "Text Time (ms)": result["text_time_ms"],
        }
        return result["image"], json.dumps(metadata, indent=2)
    else:
        return None, result["status"]

def run_interrogate(url, image, mode, categories_json):
    client = get_client(url)
    if mode == "Standard":
        res = client.interrogate(image)
    else:
        try:
            categories = json.loads(categories_json)
        except:
            return "Invalid Categories JSON"
        res = client.interrogate_structured(image, categories)
    
    return json.dumps(res, indent=2)

with gr.Blocks(title="Pi Axera SD Explorer") as demo:
    gr.Markdown("# 🥧 Pi Axera SD Interactive Explorer")
    
    with gr.Accordion("⚙️ API Configuration", open=True):
        api_url = gr.Textbox(label="API Base URL", value="http://127.0.0.1:5000", placeholder="http://pi-ip:5000")

    with gr.Tabs():
        with gr.Tab("🎨 Image Generation"):
            with gr.Row():
                with gr.Column():
                    gen_mode = gr.Radio(["txt2img", "img2img"], label="Mode", value="txt2img")
                    prompt = gr.Textbox(label="Prompt", placeholder="A red fox in the snow...", lines=3)
                    seed = gr.Number(label="Seed (-1 for random)", value=-1, precision=0)
                    
                    with gr.Group(visible=False) as i2i_params:
                        init_img = gr.Image(label="Init Image", type="pil")
                        strength = gr.Slider(label="Denoising Strength", minimum=0, maximum=1, value=0.5, step=0.01)
                        resize_mode = gr.Dropdown(
                            label="Resize Mode", 
                            choices=[("0: Stretch", 0), ("1: Crop", 1), ("2: Pad", 2)], 
                            value=0
                        )
                    
                    def toggle_i2i(m):
                        return gr.update(visible=(m == "img2img"))
                    
                    gen_mode.change(toggle_i2i, gen_mode, i2i_params)
                    
                    generate_btn = gr.Button("Generate ✨", variant="primary")
                
                with gr.Column():
                    output_img = gr.Image(label="Generated Image")
                    output_meta = gr.Code(label="Metadata", language="json")

            generate_btn.click(
                run_generate,
                inputs=[api_url, gen_mode, prompt, seed, init_img, strength, resize_mode],
                outputs=[output_img, output_meta]
            )

        with gr.Tab("🔍 Interrogation"):
            with gr.Row():
                with gr.Column():
                    inter_img = gr.Image(label="Image to Interrogate", type="pil")
                    inter_mode = gr.Radio(["Standard", "Structured"], label="Interrogation Mode", value="Standard")
                    
                    with gr.Group(visible=False) as structured_params:
                        categories_input = gr.Textbox(
                            label="Categories (JSON)", 
                            value='{"gender": ["man", "woman"], "hair": ["black", "blonde", "pink"]}',
                            lines=5
                        )
                    
                    def toggle_inter(m):
                        return gr.update(visible=(m == "Structured"))
                    
                    inter_mode.change(toggle_inter, inter_mode, structured_params)
                    
                    interrogate_btn = gr.Button("Analyze 🔎")
                
                with gr.Column():
                    inter_output = gr.Code(label="Interrogation Results", language="json")

            interrogate_btn.click(
                run_interrogate,
                inputs=[api_url, inter_img, inter_mode, categories_input],
                outputs=[inter_output]
            )

if __name__ == "__main__":
    demo.launch()
