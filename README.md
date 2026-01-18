# pi_axera_sd_interactive

Interactive web interface for exploring the Pi Axera Stable Diffusion API.

## Setup

1. Create the virtual environment (if it doesn't exist):
   ```bash
   python -m venv .venv
   ```

2. Activate the virtual environment:
   ```bash
   source .venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the application:
   ```bash
   python app.py
   ```

5. Open the provided URL (usually `http://127.0.0.1:7860`) in your browser.

## Features

- **Image Generation**: Supports txt2img and img2img modes with configurable parameters.
- **Interrogation**: Explore standard and structured image interrogation endpoints.
- **Configurable API**: Point to local or remote Pi Axera SD service instances.
