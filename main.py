from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from .routes import router

app = FastAPI(
    title="ComicCraft - AI Comic Story Creator",
    description="AI comic generation with Gemini and optional Stable Diffusion/Hugging Face.",
    version="1.0.0",
)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
app.include_router(router)
