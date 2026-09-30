import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_DIR = BASE_DIR / "static"
PANELS_DIR = STATIC_DIR / "panels"
EXPORTS_DIR = STATIC_DIR / "exports"

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()
HF_API_KEY = os.getenv("HF_API_KEY", "").strip()

# The project document names Gemini 1.5 Flash/Pro and Stable Diffusion v1.5.
# These can be changed in .env if a currently available model is preferred.
GEMINI_FLASH_MODEL = os.getenv("GEMINI_FLASH_MODEL", "gemini-1.5-flash")
GEMINI_PRO_MODEL = os.getenv("GEMINI_PRO_MODEL", "gemini-1.5-pro")
HF_IMAGE_MODEL = os.getenv(
    "HF_IMAGE_MODEL",
    "runwayml/stable-diffusion-v1-5"
)

USE_LOCAL_DIFFUSION = os.getenv("USE_LOCAL_DIFFUSION", "false").lower() == "true"

PANELS_DIR.mkdir(parents=True, exist_ok=True)
EXPORTS_DIR.mkdir(parents=True, exist_ok=True)
