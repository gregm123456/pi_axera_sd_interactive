
# Pi Axera SD Interactive Explorer

Interactive web interface for exploring and interacting with the Pi Axera Stable Diffusion API.

## Setup

1. **Create the virtual environment (if it doesn't exist):**
   ```bash
   python -m venv .venv
   ```

2. **Activate the virtual environment:**
   ```bash
   source .venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application:**
   ```bash
   python app.py
   ```

5. **Open the provided URL** (usually `http://127.0.0.1:7860`) in your browser.

---

## Features

- **Image Generation**
  - Supports both **txt2img** and **img2img** modes
  - Configurable parameters: prompt, seed, denoising strength, resize mode, and portrait enhancers
  - Upload an initial image for img2img mode
  - View and download generated images and metadata
  - Send generated images directly to interrogation or img2img workflows

- **Image Interrogation**
  - Analyze images using **Standard** and **Structured** interrogation endpoints
  - Get detailed tag scores and captions for uploaded/generated images

- **API Configuration**
  - Easily set the API base URL to point to local or remote Pi Axera SD service instances

---

## Interface Examples

### Image Generation (txt2img & img2img)

![Image Generation Example](./reference_repo_docs/pi_axera_sd_interactive_img2img_example.png)

*Example: Generating an image from a prompt and modifying an initial image using img2img mode. Metadata and workflow actions are shown below the generated image.*

### Image Interrogation

![Interrogation Example](./reference_repo_docs/pi_axera_sd_interactive_interrogation_example.png)

*Example: Interrogating a generated image to obtain tags, scores, and captions using the Standard interrogation mode.*

---

## License

See [LICENSE](LICENSE).
