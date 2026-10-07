"""Generate a square source PNG with Gemini Image on Google Cloud Agent Platform."""

import argparse
from io import BytesIO
from pathlib import Path

from google import genai
from google.genai import types
from PIL import Image


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("idea_dir", type=Path)
    parser.add_argument("--name", default="first")
    parser.add_argument("--model", default="gemini-nano-banana-2.1")
    parser.add_argument("--prompt-file", default="prompt.txt")
    parser.add_argument("--edit-source", help="Existing PNG filename inside the idea's source directory")
    parser.add_argument("--reference-image", help="Reference PNG path inside the idea directory")
    args = parser.parse_args()

    prompt = (args.idea_dir / args.prompt_file).read_text(encoding="utf-8")
    output = args.idea_dir / "source" / f"{args.name}.png"
    if output.exists():
        raise FileExistsError(f"Source image already exists: {output}")

    parts = []
    edit_source = None
    if args.edit_source:
        edit_source = args.idea_dir / "source" / args.edit_source
        parts.append(types.Part.from_bytes(data=edit_source.read_bytes(), mime_type="image/png"))
    reference_image = None
    if args.reference_image:
        reference_image = args.idea_dir / args.reference_image
        parts.append(types.Part.from_bytes(data=reference_image.read_bytes(), mime_type="image/png"))
    contents = [*parts, types.Part.from_text(text=prompt)] if parts else prompt

    client = genai.Client()
    try:
        response = client.models.generate_content(
            model=args.model,
            contents=contents,
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

    output.parent.mkdir(parents=True, exist_ok=True)
    with Image.open(BytesIO(image_part.inline_data.data)) as image:
        image.save(output, format="PNG")
    source_note = f"Edit source: {edit_source.relative_to(args.idea_dir)}\n" if edit_source else ""
    reference_note = f"Reference image: {reference_image.relative_to(args.idea_dir)}\n" if reference_image else ""
    (output.parent / f"{args.name}.prompt.txt").write_text(
        f"Model: {args.model}\n{source_note}{reference_note}\n{prompt}", encoding="utf-8"
    )
    print(f"Saved {output}")


if __name__ == "__main__":
    main()
