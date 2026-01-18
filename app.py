import gradio as gr
import json
from api_client import AxeraClient

# Portrait enhancer constants
IMAGE_PROMPT_PREFIX = "adult, face portrait photograph, "
IMAGE_PROMPT_SUFFIX = ", 8k, realistic"



# JavaScript for Cmd+Enter keyboard shortcut
shortcut_js = """
<script>
function handleKeyDown(e) {
    if (e.key === 'Enter' && (e.metaKey || e.ctrlKey)) {
        e.preventDefault();
        e.stopPropagation();

        // Sync values by blurring active element
        if (document.activeElement && document.activeElement.blur) {
            document.activeElement.blur();
        }

        try {
            const activeTab = document.querySelector('#main_tabs [role="tab"][aria-selected="true"]');
            if (activeTab && activeTab.innerText.includes('Interrogation')) {
                document.getElementById('interrogate-btn')?.click();
            } else {
                document.getElementById('generate-btn')?.click();
            }
        } catch (err) {
            document.getElementById('generate-btn')?.click();
        }
    }
}
document.addEventListener('keydown', handleKeyDown, true);
</script>
"""

def get_client(url):
    return AxeraClient(url)

def run_generate(url, mode, prompt, seed, init_image, strength, resize_mode, portrait_enhancer):
    client = get_client(url)
    if seed is None or seed == "":
        seed = -1
    
    # Apply portrait enhancers if enabled
    if portrait_enhancer:
        prompt = IMAGE_PROMPT_PREFIX + prompt + IMAGE_PROMPT_SUFFIX
    
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

    with gr.Tabs(elem_id="main_tabs") as tabs:
        with gr.Tab("🎨 Image Generation", id="tab_gen"):
            with gr.Row():
                with gr.Column():
                    gen_mode = gr.Radio(["txt2img", "img2img"], label="Mode", value="txt2img")
                    prompt = gr.Textbox(label="Prompt", placeholder="A red fox in the snow...", lines=3)
                    portrait_enhancer = gr.Checkbox(label="Add Portrait Enhancers", value=False)
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
                            value=0.75
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
                    with gr.Row():
                        send_to_i2i_btn = gr.Button("📲 Send to img2img")
                        send_to_inter_btn = gr.Button("🔍 Send to Interrogation")

            generate_btn.click(
                run_generate,
                inputs=[api_url, gen_mode, prompt, seed, init_img, strength, resize_mode, portrait_enhancer],
                outputs=[output_img, output_meta, seed]
            )

            prompt.submit(
                run_generate,
                inputs=[api_url, gen_mode, prompt, seed, init_img, strength, resize_mode, portrait_enhancer],
                outputs=[output_img, output_meta, seed]
            )

        with gr.Tab("🔍 Interrogation", id="tab_inter"):
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
                                    cat_values = gr.Textbox(label=f"Category {i+1} Values", value="agender, androgynous, bigender, genderfluid, genderqueer, man, non-binary, transgender, two-spirit, woman")
                                elif i == 1:
                                    cat_name = gr.Textbox(label=f"Category {i+1} Name", value="hair")
                                    cat_values = gr.Textbox(label=f"Category {i+1} Values", value="auburn hair, black hair, blonde hair, blue hair, brown hair, chestnut hair, ginger hair, gray hair, green hair, pink hair, purple hair, red hair, white hair")
                                else:
                                    cat_name = gr.Textbox(label=f"Category {i+1} Name", placeholder="e.g., gender")
                                    cat_values = gr.Textbox(label=f"Category {i+1} Values", placeholder="e.g., agender, androgynous, bigender, genderfluid, genderqueer, man, non-binary, transgender, two-spirit, woman")
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

            # Image transfer logic
            send_to_i2i_btn.click(
                fn=lambda x: (x, "img2img"),
                inputs=[output_img],
                outputs=[init_img, gen_mode]
            )
            
            send_to_inter_btn.click(
                fn=lambda x: x,
                inputs=[output_img],
                outputs=[inter_img],
                js="""
                (x) => {
                    setTimeout(() => {
                        const tabButtons = document.querySelectorAll('#main_tabs .tab-nav button');
                        if (tabButtons && tabButtons[1]) {
                            tabButtons[1].click();
                        } else {
                            // Fallback to text matching if structure is different
                            const allTabs = Array.from(document.querySelectorAll('button[role="tab"]'));
                            const interTab = allTabs.find(b => b.textContent.includes('Interrogation'));
                            if (interTab) interTab.click();
                        }
                    }, 50);
                    return x;
                }
                """
            )

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", head=shortcut_js)
