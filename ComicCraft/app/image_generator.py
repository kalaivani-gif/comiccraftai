import re
import requests
from pathlib import Path

from .config import PANELS_DIR


def _safe_name(text):
    text = re.sub(
        r"[^a-zA-Z0-9_-]+",
        "_",
        text
    ).strip("_")

    return text[:60] or "panel"


def _download_test_image(panel_number):
    """
    Downloads a test image from the internet
    and saves it inside static/panels.
    """

    image_url = (
        f"https://placehold.co/1024x768/png"
        f"?text=ComicCraft+Panel+{panel_number}"
    )

    response = requests.get(
        image_url,
        timeout=30
    )

    response.raise_for_status()

    filename = (
        f"panel_{panel_number}_ComicCraft_Test.png"
    )

    path = PANELS_DIR / filename

    path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(path, "wb") as file:
        file.write(response.content)

    return str(path)


def generate_image(prompt, panel_number):
    """
    Generate/download an image for each comic panel.

    For testing, this uses an online image URL.
    """

    try:
        return _download_test_image(panel_number)

    except Exception as exc:
        print(
            f"Test image download failed for panel "
            f"{panel_number}: {exc}"
        )

        # Local fallback image
        from PIL import Image, ImageDraw

        img = Image.new(
            "RGB",
            (1024, 768),
            "white"
        )

        draw = ImageDraw.Draw(img)

        draw.rectangle(
            (25, 25, 999, 743),
            outline="black",
            width=5
        )

        draw.text(
            (55, 55),
            f"ComicCraft - Panel {panel_number}",
            fill="black"
        )

        draw.text(
            (55, 150),
            prompt[:100],
            fill="black"
        )

        filename = (
            f"panel_{panel_number}_fallback.png"
        )

        path = PANELS_DIR / filename

        path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        img.save(path)

        return str(path)