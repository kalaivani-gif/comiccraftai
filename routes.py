from fastapi import APIRouter, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse

from .models import PromptRequest
from .gemini_flash import generate_outline
from .gemini_pro import generate_story
from .image_generator import generate_image
from .layout_builder import build_comic_layout
from .exporters import save_pdf
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")

router = APIRouter()

@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@router.post("/generate", response_class=HTMLResponse)
async def generate(
    request: Request,
    story_prompt: str = Form(...),
    character_name: str = Form(...),
    setting: str = Form(...),
    tone: str = Form(...),
    art_style: str = Form(...),
):
    try:
        outline = generate_outline(story_prompt, character_name, setting, tone, art_style)
        story = generate_story(outline, character_name, tone)
        images = [
            generate_image(panel["image_prompt"], panel["panel_number"])
            for panel in outline
        ]
        layout = build_comic_layout(outline, story, images)
        pdf_path = save_pdf(layout)

        public_pdf = "/" + pdf_path.replace("\\", "/").split("static/", 1)[-1]
        return templates.TemplateResponse(
            "comic_preview.html",
            {"request": request, "layout": layout, "pdf_path": public_pdf}
        )
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))

@router.post("/generate-comic/json")
async def generate_json(payload: PromptRequest):
    outline = generate_outline(
        payload.story_prompt, payload.character_name,
        payload.setting, payload.tone, payload.art_style
    )
    story = generate_story(outline, payload.character_name, payload.tone)
    images = [generate_image(p["image_prompt"], p["panel_number"]) for p in outline]
    layout = build_comic_layout(outline, story, images)
    pdf_path = save_pdf(layout)
    public_pdf = "/" + pdf_path.replace("\\", "/").split("static/", 1)[-1]
    return JSONResponse({"layout": layout, "pdf_path": public_pdf})

@router.get("/test-image", response_class=HTMLResponse)
async def test_image(prompt: str = "A brave fox in an enchanted forest, comic book style"):
    path = generate_image(prompt, 1)
    public_path = "/" + path.replace("\\", "/").split("static/", 1)[-1]
    return f'<html><body><h1>ComicCraft Image Test</h1><img src="{public_path}" style="max-width:800px"><p>{prompt}</p><p><a href="/">Back</a></p></body></html>'

@router.get("/export-success", response_class=HTMLResponse)
async def export_success(request: Request):
    return templates.TemplateResponse("export_success.html", {"request": request})
