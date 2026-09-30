import os
from dotenv import load_dotenv
load_dotenv()

class GeminiDocumentGenerator:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.model = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
        self.client = None
        if self.api_key:
            try:
                from google import genai
                self.client = genai.Client(api_key=self.api_key)
            except Exception:
                self.client = None

    def generate_document(self, document_type, parties, terms, dates):
        if not self.api_key or not self.client:
            raise RuntimeError("GEMINI_API_KEY is missing. Create .env and add your Gemini API key.")
        prompt = f'''You are LegalEase, an AI assistant for drafting structured legal documents.
Create a professional DRAFT of the requested legal document.

Document type: {document_type}
Parties involved: {parties}
Terms and conditions: {terms}
Effective date: {dates}

Requirements:
- Use clear formal legal language.
- Include a title and appropriate sections.
- Reflect supplied parties, terms and date accurately.
- Do not invent personal details.
- Use [INSERT DETAILS] for essential missing information.
- Include signature blocks where appropriate.
- Return plain text with readable headings.
- State that it should be reviewed by a qualified legal professional before use.
'''
        response = self.client.models.generate_content(model=self.model, contents=prompt)
        text = getattr(response, "text", None)
        if not text:
            raise RuntimeError("Gemini returned an empty response.")
        return text.strip()
