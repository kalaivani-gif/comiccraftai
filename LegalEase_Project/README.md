# LegalEase
FastAPI backend + Streamlit frontend + Google Gemini + TXT/DOCX/PDF export.

## Setup
1. Install Python 3.10+.
2. Open this folder in VS Code.
3. Create a virtual environment: `python -m venv .venv`
4. Activate it.
5. Install: `pip install -r requirements.txt`
6. Copy `.env.example` to `.env` and add your Gemini API key.
7. Terminal 1: `uvicorn backend.main:app --reload`
8. Terminal 2: `streamlit run frontend/app.py`
9. Open the Streamlit URL shown in the terminal.

The supplied document specifies FastAPI, Streamlit, Gemini, editable preview and TXT/DOCX/PDF export. This implementation follows that architecture. 
