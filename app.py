import gradio as gr
import json
from api_client import AxeraClient

# JavaScript for Cmd+Enter keyboard shortcut
shortcut_js = """
<script>
function handleKeyDown(e) {
    // Check if Enter is pressed with Cmd (metaKey) or Ctrl
    if (e.key === 'Enter' && (e.metaKey || e.ctrlKey)) {
        // Prevent default behavior
        e.preventDefault();
        // Try to click the interrogate button first (if on interrogation tab)
        const interrogateBtn = document.getElementById('interrogate-btn');
        if (interrogateBtn) {
            interrogateBtn.click();
        } else {
            // Otherwise click the generate button
            const generateBtn = document.getElementById('generate-btn');
            if (generateBtn) {
                generateBtn.click();
            }
        }
    }
}
document.addEventListener('keydown', handleKeyDown, false);
</script>
"""

def get_client(url):
    return AxeraClient(url)

def run_generate(url, mode, prompt, seed, init_image, strength, resize_mode):
    client = get_client(url)
    if seed is None or seed == "":
        seed = -1
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
        return result["image"], json.dumps(metadata, indent=2), seed
    else:
        return None, result["status"], seed

def run_interrogate(url, image, mode, *category_inputs):
    client = get_client(url)
    if mode == "Standard":
        res = client.interrogate(image)
    else:
        categories = {}
        for i in range(0, len(category_inputs), 2):
            name = category_inputs[i]
            values_str = category_inputs[i+1]
            if name.strip() and values_str.strip():
                categories[name.strip()] = [v.strip() for v in values_str.split(',') if v.strip()]
        if not categories:
            return "No valid categories provided"
        res = client.interrogate_structured(image, categories)
    
    return json.dumps(res, indent=2)

with gr.Blocks(title="Pi Axera SD Explorer") as demo:
    gr.Markdown("# 🥧 Pi Axera SD Interactive Explorer")
    
    with gr.Accordion("⚙️ API Configuration", open=True):
        api_url = gr.Textbox(label="API Base URL", value="http://m5:5000", placeholder="http://pi-ip:5000")

    with gr.Tabs():
        with gr.Tab("🎨 Image Generation"):
            with gr.Row():
                with gr.Column():
                    gen_mode = gr.Radio(["txt2img", "img2img"], label="Mode", value="txt2img")
                    prompt = gr.Textbox(label="Prompt", placeholder="A red fox in the snow...", lines=3)
                    seed = gr.Number(label="Seed (-1 for random)", value=-1, precision=0)
                    
                    with gr.Group(visible=False) as i2i_params:
                        init_img = gr.Image(label="Init Image", type="pil")
                        strength = gr.Dropdown(
                            label="Denoising Strength", 
                            choices=[
                                ("0.25: Minimal changes (1 step)", 0.25),
                                ("0.50: Balanced (2 steps)", 0.5),
                                ("0.75: Strong modification (3 steps)", 0.75),
                                ("1.00: Complete reimagining (4 steps)", 1.0)
                            ], 
                            value=0.5
                        )
                        resize_mode = gr.Dropdown(
                            label="Resize Mode", 
                            choices=[("0: Stretch", 0), ("1: Crop", 1), ("2: Pad", 2)], 
                            value=0
                        )
                    
                    def toggle_i2i(m):
                        return gr.update(visible=(m == "img2img"))
                    
                    gen_mode.change(toggle_i2i, gen_mode, i2i_params)
                    
                    generate_btn = gr.Button("Generate ✨", variant="primary", elem_id="generate-btn")
                
                with gr.Column():
                    output_img = gr.Image(label="Generated Image")
                    output_meta = gr.Code(label="Metadata", language="json")

            generate_btn.click(
                run_generate,
                inputs=[api_url, gen_mode, prompt, seed, init_img, strength, resize_mode],
                outputs=[output_img, output_meta, seed]
            )
            
            prompt.submit(
                run_generate,
                inputs=[api_url, gen_mode, prompt, seed, init_img, strength, resize_mode],
                outputs=[output_img, output_meta, seed]
            )

        with gr.Tab("🔍 Interrogation"):
            with gr.Row():
                with gr.Column():
                    inter_img = gr.Image(label="Image to Interrogate", type="pil")
                    inter_mode = gr.Radio(["Standard", "Structured"], label="Interrogation Mode", value="Standard")
                    
                    with gr.Group(visible=False) as structured_params:
                        gr.Markdown("Add categories below (leave empty to skip):")
                        categories_components = []
                        for i in range(10):
                            with gr.Row():
                                if i == 0:
                                    cat_name = gr.Textbox(label=f"Category {i+1} Name", value="gender")
                                    cat_values = gr.Textbox(label=f"Category {i+1} Values", value="man, woman")
                                elif i == 1:
                                    cat_name = gr.Textbox(label=f"Category {i+1} Name", value="hair")
                                    cat_values = gr.Textbox(label=f"Category {i+1} Values", value="black, blonde, pink")
                                else:
                                    cat_name = gr.Textbox(label=f"Category {i+1} Name", placeholder="e.g., gender")
                                    cat_values = gr.Textbox(label=f"Category {i+1} Values", placeholder="e.g., man, woman")
                            categories_components.extend([cat_name, cat_values])
                    
                    def toggle_inter(m):
                        return gr.update(visible=(m == "Structured"))
                    
                    inter_mode.change(toggle_inter, inter_mode, structured_params)
                    
                    interrogate_btn = gr.Button("Analyze 🔎", elem_id="interrogate-btn")
                
                with gr.Column():
                    inter_output = gr.Code(label="Interrogation Results", language="json")

            interrogate_btn.click(
                run_interrogate,
                inputs=[api_url, inter_img, inter_mode] + categories_components,
                outputs=[inter_output]
            )

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", head=shortcut_js)
