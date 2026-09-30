import json
import re
from .config import GEMINI_API_KEY, GEMINI_FLASH_MODEL

def _fallback_outline(story_prompt, character_name, setting, tone, art_style):
    scenes = [
        ("The Beginning", f"{character_name} starts the adventure in {setting}."),
        ("A New Discovery", f"{character_name} discovers something unexpected in {setting}."),
        ("The Challenge", f"A difficult challenge appears and tests {character_name}."),
        ("The Turning Point", f"{character_name} finds a clever way forward."),
        ("The Ending", f"{character_name} completes the adventure with a memorable lesson.")
    ]
    return [
        {
            "panel_number": i + 1,
            "title": title,
            "scene_description": desc,
            "image_prompt": (
                f"{art_style} comic panel, {setting}, {desc} "
                f"Main character: {character_name}. Tone: {tone}. "
                "cinematic composition, expressive characters, clean comic illustration."
            ),
        }
        for i, (title, desc) in enumerate(scenes)
    ]

def generate_outline(story_prompt, character_name, setting, tone, art_style):
    if not GEMINI_API_KEY:
        return _fallback_outline(story_prompt, character_name, setting, tone, art_style)

    try:
        import google.generativeai as genai
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel(GEMINI_FLASH_MODEL)
        prompt = f"""
Create a structured 5-panel comic outline.

Story prompt: {story_prompt}
Main character: {character_name}
Setting: {setting}
Tone: {tone}
Art style: {art_style}

Return ONLY valid JSON as an array of exactly 5 objects.
Each object must contain:
panel_number, title, scene_description, image_prompt.
"""
        response = model.generate_content(prompt)
        text = response.text.strip()
        text = re.sub(r"^```json\s*|\s*```$", "", text, flags=re.I)
        data = json.loads(text)
        if isinstance(data, list) and len(data) >= 5:
            return data[:5]
    except Exception:
        pass

    return _fallback_outline(story_prompt, character_name, setting, tone, art_style)
