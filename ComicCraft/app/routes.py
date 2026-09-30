from fastapi import APIRouter, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates

from .models import PromptRequest
from .gemini_flash import generate_outline
from .gemini_pro import generate_story
from .image_generator import generate_image
from .layout_builder import build_comic_layout
from .exporters import save_pdf


templates = Jinja2Templates(directory="templates")

router = APIRouter()


# ==========================================
# HOME PAGE
# ==========================================

@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        request,
        "index.html"
    )


# ==========================================
# GENERATE COMIC
# ==========================================

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

        # ----------------------------------
        # STEP 1 - Generate Outline
        # ----------------------------------

        print("STEP 1: Generating outline...")

        outline = generate_outline(
            story_prompt,
            character_name,
            setting,
            tone,
            art_style
        )

        print("STEP 1 DONE")


        # ----------------------------------
        # STEP 2 - Generate Story
        # ----------------------------------

        print("STEP 2: Generating story...")

        story = generate_story(
            outline,
            character_name,
            tone
        )

        print("STEP 2 DONE")


        # ----------------------------------
        # STEP 3 - Generate Images
        # ----------------------------------

        print("STEP 3: Generating images...")

        images = []

        for panel in outline:

            image = generate_image(
                panel["image_prompt"],
                panel["panel_number"]
            )

            images.append(image)

        print("STEP 3 DONE")


        # ----------------------------------
        # STEP 4 - Build Comic Layout
        # ----------------------------------

        print("STEP 4: Building comic layout...")

        layout = build_comic_layout(
            outline,
            story,
            images
        )

        print("STEP 4 DONE")


        # ----------------------------------
        # STEP 5 - Generate PDF
        # ----------------------------------

        print("STEP 5: Generating PDF...")

        pdf_path = save_pdf(layout)

        print("STEP 5 DONE:", pdf_path)


        # ----------------------------------
        # SHOW COMIC PREVIEW
        # ----------------------------------

        return templates.TemplateResponse(
            request,
            "comic_preview.html",
            {
                "layout": layout,
                "pdf_path": pdf_path
            }
        )


    except Exception as exc:

        print("===================================")
        print("COMIC GENERATION ERROR")
        print("===================================")
        print(str(exc))
        print("===================================")

        raise HTTPException(
            status_code=500,
            detail=str(exc)
        )


# ==========================================
# JSON GENERATE COMIC
# ==========================================

@router.post("/generate-comic/json")
async def generate_json(payload: PromptRequest):

    try:

        print("STEP 1: Generating outline...")

        outline = generate_outline(
            payload.story_prompt,
            payload.character_name,
            payload.setting,
            payload.tone,
            payload.art_style
        )

        print("STEP 1 DONE")


        print("STEP 2: Generating story...")

        story = generate_story(
            outline,
            payload.character_name,
            payload.tone
        )

        print("STEP 2 DONE")


        print("STEP 3: Generating images...")

        images = []

        for panel in outline:

            image = generate_image(
                panel["image_prompt"],
                panel["panel_number"]
            )

            images.append(image)

        print("STEP 3 DONE")


        print("STEP 4: Building comic layout...")

        layout = build_comic_layout(
            outline,
            story,
            images
        )

        print("STEP 4 DONE")


        # ----------------------------------
        # STEP 5 - Generate PDF
        # ----------------------------------

        print("STEP 5: Generating PDF...")

        pdf_path = save_pdf(layout)

        print("STEP 5 DONE:", pdf_path)


        return JSONResponse(
            {
                "layout": layout,
                "pdf_path": pdf_path
            }
        )


    except Exception as exc:

        print("===================================")
        print("JSON GENERATION ERROR")
        print("===================================")
        print(str(exc))
        print("===================================")

        raise HTTPException(
            status_code=500,
            detail=str(exc)
        )


# ==========================================
# TEST IMAGE
# ==========================================

@router.get(
    "/test-image",
    response_class=HTMLResponse
)
async def test_image(
    prompt: str = "A brave fox in an enchanted forest, comic book style"
):

    try:

        path = generate_image(
            prompt,
            1
        )

        public_path = "/" + path.replace(
            "\\",
            "/"
        ).split("static/", 1)[-1]

        return f"""
        <html>
            <body>

                <h1>ComicCraft Image Test</h1>

                <img
                    src="{public_path}"
                    style="max-width:800px"
                >

                <p>{prompt}</p>

                <p>
                    <a href="/">Back</a>
                </p>

            </body>
        </html>
        """

    except Exception as exc:

        return f"""
        <html>
            <body>

                <h1>Image Generation Error</h1>

                <p>{str(exc)}</p>

                <p>
                    <a href="/">Back</a>
                </p>

            </body>
        </html>
        """


# ==========================================
# EXPORT SUCCESS
# ==========================================

@router.get(
    "/export-success",
    response_class=HTMLResponse
)
async def export_success(request: Request):

    return templates.TemplateResponse(
        request,
        "export_success.html"
    )