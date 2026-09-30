from pathlib import Path


def build_comic_layout(outline, story, image_paths):

    story_by_panel = {
        item["panel_number"]: item
        for item in story
    }

    layout = []

    for item, image_path in zip(outline, image_paths):

        story_item = story_by_panel.get(
            item["panel_number"],
            {}
        )

        # Convert Windows full path into browser-friendly URL
        image_filename = Path(image_path).name

        image_url = f"/static/panels/{image_filename}"

        layout.append({

            "panel_number": item["panel_number"],

            "title": item["title"],

            "image_path": image_url,

            "scene_description": item["scene_description"],

            "image_prompt": item["image_prompt"],

            "caption": story_item.get(
                "caption",
                ""
            ),

            "narration": story_item.get(
                "narration",
                ""
            ),

            "dialogue": story_item.get(
                "dialogue",
                ""
            ),
        })

    return layout