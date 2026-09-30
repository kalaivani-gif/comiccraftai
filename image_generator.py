import base64
import io
import re
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

from .config import HF_API_KEY, HF_IMAGE_MODEL, PANELS_DIR, USE_LOCAL_DIFFUSION

def _safe_name(text):
    text = re.sub(r"[^a-zA-Z0-9_-]+", "_", text).strip("_")
    return text[:60] or "panel"

def _placeholder(prompt, panel_number):
    img = Image.new("RGB", (1024, 768), "white")
    draw = ImageDraw.Draw(img)
    title = f"ComicCraft - Panel {panel_number}"
    draw.rectangle((25, 25, 999, 743), outline="black", width=5)
    draw.text((55, 55), title, fill="black")
    # Keep the placeholder readable on systems without an image-generation API.
    words = prompt.split()
    lines, line = [], ""
    for w in words:
        if len(line) + len(w) + 1 > 65:
            lines.append(line)
            line = w
        else:
            line = (line + " " + w).strip()
    if line:
        lines.append(line)
    y = 150
    for line in lines[:18]:
        draw.text((55, y), line, fill="black")
        y += 28
    path = PANELS_DIR / f"panel_{panel_number}_{_safe_name(title)}.png"
    img.save(path)
    return str(path)

def _hf_image(prompt, panel_number):
    import requests
    url = f"https://api-inference.huggingface.co/models/{HF_IMAGE_MODEL}"
    headers = {"Authorization": f"Bearer {HF_API_KEY}"}
    response = requests.post(url, headers=headers, json={"inputs": prompt}, timeout=180)
    response.raise_for_status()
    image = Image.open(io.BytesIO(response.content)).convert("RGB")
    path = PANELS_DIR / f"panel_{panel_number}_{_safe_name(prompt)}.png"
    image.save(path)
    return str(path)

def _local_diffusion(prompt, panel_number):
    from diffusers import StableDiffusionPipeline
    import torch
    pipe = StableDiffusionPipeline.from_pretrained(HF_IMAGE_MODEL)
    if torch.cuda.is_available():
        pipe = pipe.to("cuda")
    image = pipe(prompt).images[0]
    path = PANELS_DIR / f"panel_{panel_number}_{_safe_name(prompt)}.png"
    image.save(path)
    return str(path)

def generate_image(prompt, panel_number):
    if HF_API_KEY:
        try:
            return _hf_image(prompt, panel_number)
        except Exception:
            pass
    if USE_LOCAL_DIFFUSION:
        try:
            return _local_diffusion(prompt, panel_number)
        except Exception:
            pass
    return _placeholder(prompt, panel_number)
