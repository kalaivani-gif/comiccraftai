from .config import GEMINI_API_KEY, GEMINI_PRO_MODEL

def _fallback_story(outline, character_name, tone):
    panels = []
    for p in outline:
        n = p["panel_number"]
        panels.append({
            "panel_number": n,
            "title": p["title"],
            "caption": f"Panel {n}: The story continues.",
            "narration": p["scene_description"],
            "dialogue": f'{character_name}: "I will keep going!"'
        })
    return panels

def generate_story(outline, character_name, tone):
    if not GEMINI_API_KEY:
        return _fallback_story(outline, character_name, tone)

    try:
        import google.generativeai as genai
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel(GEMINI_PRO_MODEL)
        prompt = f"""
Expand this 5-panel comic outline into engaging comic narration and dialogue.

Character: {character_name}
Tone: {tone}
Outline:
{outline}

Return ONLY valid JSON as an array. For every panel include:
panel_number, title, caption, narration, dialogue.
"""
        response = model.generate_content(prompt)
        import json, re
        text = re.sub(r"^```json\s*|\s*```$", "", response.text.strip(), flags=re.I)
        data = json.loads(text)
        if isinstance(data, list) and len(data) >= 5:
            return data[:5]
    except Exception:
        pass

    return _fallback_story(outline, character_name, tone)
