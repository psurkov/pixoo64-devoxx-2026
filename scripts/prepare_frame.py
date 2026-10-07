"""Turn one source image into a native Pixoo frame and a review preview."""

import argparse
import hashlib
import json
from pathlib import Path

from PIL import Image, ImageEnhance


SIZE = 64
PREVIEW_SCALE = 8


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("idea_dir", type=Path)
    parser.add_argument("source_name", help="PNG filename inside the idea's source directory")
    parser.add_argument("--frame", default="frame_001.png")
    parser.add_argument("--crop", nargs=4, type=int, metavar=("LEFT", "TOP", "RIGHT", "BOTTOM"))
    parser.add_argument("--contrast", type=float, default=1.15)
    parser.add_argument("--colors", type=int, default=32)
    args = parser.parse_args()

    source_path = args.idea_dir / "source" / args.source_name
    source_bytes = source_path.read_bytes()
    with Image.open(source_path) as source:
        image = source.convert("RGB")

    if args.crop:
        left, top, right, bottom = args.crop
    else:
        side = min(image.width, image.height)
        left = (image.width - side) // 2
        top = (image.height - side) // 2
        right, bottom = left + side, top + side

    if right <= left or right - left != bottom - top or left < 0 or top < 0 or right > image.width or bottom > image.height:
        raise ValueError("Crop must be a square inside the source image")
    if args.contrast <= 0 or not 2 <= args.colors <= 256:
        raise ValueError("Contrast must be positive and colors must be between 2 and 256")

    image = image.crop((left, top, right, bottom))
    image = ImageEnhance.Contrast(image).enhance(args.contrast)
    image = image.resize((SIZE, SIZE), Image.Resampling.BOX)
    image = image.quantize(
        colors=args.colors,
        method=Image.Quantize.MEDIANCUT,
        dither=Image.Dither.NONE,
    ).convert("RGB")

    frame_path = args.idea_dir / "frames" / args.frame
    preview_path = args.idea_dir / "review" / f"{Path(args.frame).stem}-8x.png"
    recipe_path = frame_path.with_suffix(".recipe.json")
    frame_path.parent.mkdir(parents=True, exist_ok=True)
    preview_path.parent.mkdir(parents=True, exist_ok=True)

    image.save(frame_path)
    image.resize((SIZE * PREVIEW_SCALE, SIZE * PREVIEW_SCALE), Image.Resampling.NEAREST).save(preview_path)
    recipe_path.write_text(
        json.dumps({
            "source": str(source_path.relative_to(args.idea_dir)),
            "source_sha256": hashlib.sha256(source_bytes).hexdigest(),
            "crop": [left, top, right, bottom],
            "contrast": args.contrast,
            "colors": args.colors,
            "downsample": "box",
            "quantization": "median_cut_without_dithering",
            "preview_scale": PREVIEW_SCALE,
        }, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"Frame: {frame_path}\nReview preview: {preview_path}\nRecipe: {recipe_path}")


if __name__ == "__main__":
    main()
