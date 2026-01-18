import requests
import base64
import io
from PIL import Image

def image_to_base64(img):
    """Convert a PIL Image to a base64 string."""
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode('utf-8')

def base64_to_image(b64_str):
    """Convert a base64 string back to a PIL Image."""
    img_data = base64.b64decode(b64_str)
    return Image.open(io.BytesIO(img_data))

class AxeraClient:
    def __init__(self, base_url):
        self.base_url = base_url.rstrip('/')

    def generate(self, mode, prompt, seed=-1, init_image=None, denoising_strength=0.5, resize_mode=0):
        url = f"{self.base_url}/generate"
        
        payload = {
            "mode": mode,
            "prompt": prompt,
            "seed": seed
        }
        
        if mode == "img2img" and init_image is not None:
            payload["init_image"] = image_to_base64(init_image)
            payload["denoising_strength"] = denoising_strength
            payload["resize_mode"] = resize_mode
            
        try:
            response = requests.post(url, json=payload, timeout=60)
            response.raise_for_status()
            data = response.json()
            
            if data.get("status") == "ok":
                img = base64_to_image(data["base64"])
                return {
                    "image": img,
                    "seed": data.get("seed"),
                    "total_time_ms": data.get("total_time_ms"),
                    "text_time_ms": data.get("text_time_ms"),
                    "status": "Success"
                }
            else:
                return {"status": f"Error: {data.get('error', 'Unknown error')}"}
        except Exception as e:
            return {"status": f"Connection Error: {str(e)}"}

    def interrogate(self, image):
        url = f"{self.base_url}/sdapi/v1/interrogate"
        payload = {"image": image_to_base64(image)}
        
        try:
            response = requests.post(url, json=payload, timeout=30)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"error": str(e)}

    def interrogate_structured(self, image, categories):
        url = f"{self.base_url}/sdapi/v1/interrogate/structured"
        payload = {
            "image": image_to_base64(image),
            "categories": categories
        }
        
        try:
            response = requests.post(url, json=payload, timeout=30)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"error": str(e)}
