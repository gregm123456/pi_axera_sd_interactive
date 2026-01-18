# Implementation Plan: Pi Axera SD Interactive Explorer

This document outlines the strategy for building a interactive web interface for the Pi Axera Stable Diffusion service.

## 1. Core Architecture
- **Framework**: Gradio (for rapid UI prototyping and native image handling).
- **Backend Communication**: A standalone Python client that interfaces with the `/generate` and `/sdapi` endpoints.
- **Configurability**: Support for dynamic API URL/Port selection to allow connecting to local or remote Pi hardware.

## 2. Features & Components

### A. Global Configuration
- **API URL**: Text input for the host (e.g., `http://192.168.1.100:5000`).

### B. Image Generation Tab
- **Mode Toggle**: `txt2img` vs `img2img`.
- **Primary Inputs**:
    - Prompt (Textbox)
    - Seed (Number, default -1 for random)
- **img2img Specifics**:
    - Image Upload
    - Denoising Strength (Slider 0.0 - 1.0)
    - **Resize Mode Dropdown**:
        - 0: Stretch (Default)
        - 1: Crop (Center crop to 512x512)
        - 2: Pad (Letterbox/Fill to 512x512)
- **Output Area**:
    - Resulting Image
    - Generation Metadata (Total Time, Text Time, Final Seed)

### C. Image Interrogation Tab
- **Endpoint Selection**: Standard Top-K vs Structured.
- **Standard Interrogation**:
    - Upload image -> Get flat tags and scores.
- **Structured Classification**:
    - Upload image.
    - Category Input: A JSON-style textbox for defining classification groups (e.g., `{"gender": ["man", "woman"], "hair": ["black", "blonde"]}`).
    - Results: Display winner and confidence for each category + general tags.

## 3. Implementation Steps
1. **API Client (`api_client.py`)**:
    - Function `generate_image(params, base_url)`
    - Function `interrogate(image, mode, categories, base_url)`
2. **Main Application (`app.py`)**:
    - Define Gradio Layout (Tabs/Accordions).
    - Handle State: Manage the API base URL.
    - Wire Events: Map button clicks to the client functions.
3. **Execution**:
    - Run `python app.py` and share via local URL or Gradio's public link feature.
