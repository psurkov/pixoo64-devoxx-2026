"""Generate a square source PNG with Gemini Image on Google Cloud Agent Platform."""

import argparse
from io import BytesIO
from pathlib import Path

from google import genai
from google.genai import types
from PIL import Image


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("prompt_file", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--model", default="gemini-nano-banana-2.1")
    args = parser.parse_args()

    prompt = args.prompt_file.read_text(encoding="utf-8")
    client = genai.Client()
    try:
        response = client.models.generate_content(
            model=args.model,
            contents=prompt,
            config=types.GenerateContentConfig(
                response_modalities=["IMAGE"],
                image_config=types.ImageConfig(aspect_ratio="1:1"),
            ),
        )
    finally:
        client.close()

    image_part = next((part for part in response.parts if part.inline_data), None)
    if image_part is None:
        raise RuntimeError("The model returned no image")

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with Image.open(BytesIO(image_part.inline_data.data)) as image:
        image.save(args.output, format="PNG")
    print(f"Saved {args.output}")


if __name__ == "__main__":
    main()
