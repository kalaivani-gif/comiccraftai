# ComicCraft - AI Comic Story Creator

ComicCraft is a FastAPI web application based on the supplied project document.

## Features
- Story prompt, character, setting, tone and art-style inputs
- 5-panel structured comic outline
- Gemini-based narration/dialogue when a Gemini API key is configured
- Optional Hugging Face Stable Diffusion image generation
- Lightweight fallback images when APIs are not configured
- Comic preview page
- PDF export using FPDF
- JSON API endpoint and image-test endpoint

## Project structure
```text
ComicCraft/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── routes.py
│   ├── models.py
│   ├── config.py
│   ├── gemini_flash.py
│   ├── gemini_pro.py
│   ├── image_generator.py
│   ├── layout_builder.py
│   └── exporters.py
├── templates/
│   ├── index.html
│   ├── comic_preview.html
│   └── export_success.html
├── static/
│   ├── css/style.css
│   ├── js/
│   ├── panels/
│   └── exports/
├── requirements.txt
├── requirements-diffusers.txt
├── .env.example
└── README.md
```

## Windows setup
```bat
python -m venv env
env\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
copy .env.example .env
uvicorn app.main:app --reload
```

Open:
- http://127.0.0.1:8000
- http://127.0.0.1:8000/docs

## API keys
The app works in fallback/demo mode without keys.

For Gemini:
1. Create a Gemini API key.
2. Put it in `.env` as `GEMINI_API_KEY=...`.
3. If your account does not provide the document's Gemini 1.5 model names, change the model names in `.env` to models available to your account.

For image generation:
- Add `HF_API_KEY` for Hugging Face Inference API.
- Or install `requirements-diffusers.txt` and set `USE_LOCAL_DIFFUSION=true` for local Stable Diffusion. This is much heavier and usually needs a capable GPU.

## Main routes
- `GET /` - homepage
- `POST /generate` - form-based comic generation
- `POST /generate-comic/json` - JSON API
- `GET /test-image` - image generation test
- `GET /export-success` - export confirmation page
