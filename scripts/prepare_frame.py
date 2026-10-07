"""Turn one source image into a native Pixoo frame and a review preview."""

import argparse
import hashlib
import json
from pathlib import Path

import numpy as np
from PIL import Image, ImageEnhance, ImageFilter

SIZE = 64
PREVIEW_SCALE = 8
WORKING_COLORS = 48


def square_crop(image: Image.Image, crop: list[int] | None) -> tuple[int, int, int, int]:
    if crop:
        left, top, right, bottom = crop
    else:
        side = min(image.width, image.height)
        left = (image.width - side) // 2
        top = (image.height - side) // 2
        right, bottom = left + side, top + side
    if (
        right <= left
        or right - left != bottom - top
        or left < 0
        or top < 0
        or right > image.width
        or bottom > image.height
    ):
        raise ValueError("Crop must be a square inside the source image")
    return left, top, right, bottom


def flatten_texture(image: Image.Image, strength: float) -> Image.Image:
    """Replace fine texture with the locally dominant color before the cell size is decided.

    Hair strands, wood grain and leaf veins are smaller than one output pixel. Left in place they
    make neighbouring cells pick different dominant colors, which reads as speckle. Flattening
    them first keeps each object a single mass.
    """
    cell = image.width / SIZE
    size = int(cell * strength) | 1
    return image.filter(ImageFilter.ModeFilter(size)) if size >= 3 else image


def downsample_mode(image: Image.Image, working_colors: int) -> Image.Image:
    """Give each output pixel the color that covers most of its cell.

    Averaging blends neighbouring color masses into mud; point sampling keeps one arbitrary
    pixel per cell and turns anti-aliased edges into noise. Collapsing the anti-aliasing into a
    working palette first and then taking the dominant color per cell keeps hard edges while
    still reading the whole cell.
    """
    side = image.width - image.width % SIZE
    if side < SIZE:
        raise ValueError("Source is smaller than the 64x64 target")
    image = image.resize((side, side), Image.Resampling.LANCZOS) if side != image.width else image

    working = image.quantize(
        colors=working_colors, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE
    )
    palette = np.asarray(working.getpalette(), dtype=np.uint8).reshape(-1, 3)
    cell = side // SIZE
    indices = np.asarray(working, dtype=np.int64).reshape(SIZE, cell, SIZE, cell)
    indices = indices.transpose(0, 2, 1, 3).reshape(SIZE, SIZE, cell * cell)

    counts = np.zeros((SIZE, SIZE, len(palette)), dtype=np.int32)
    np.add.at(
        counts,
        (
            np.arange(SIZE)[:, None, None],
            np.arange(SIZE)[None, :, None],
            indices,
        ),
        1,
    )
    dominant = counts.argmax(axis=2)
    return Image.fromarray(palette[dominant], mode="RGB")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("idea_dir", type=Path)
    parser.add_argument("source_name", help="PNG filename inside the idea's source directory")
    parser.add_argument("--frame", default="frame_001.png")
    parser.add_argument("--crop", nargs=4, type=int, metavar=("LEFT", "TOP", "RIGHT", "BOTTOM"))
    parser.add_argument(
        "--downsample",
        choices=("mode", "box"),
        default="mode",
        help="mode keeps each cell's dominant color; box averages it and reads softer",
    )
    parser.add_argument(
        "--flatten",
        type=float,
        default=0.55,
        help="local-dominant-color radius as a fraction of one output cell; 0 disables it",
    )
    parser.add_argument("--contrast", type=float, default=1.1)
    parser.add_argument("--saturation", type=float, default=1.05)
    parser.add_argument(
        "--sharpen",
        type=float,
        default=0.3,
        help="unsharp strength applied before downsampling, to hold silhouettes",
    )
    parser.add_argument("--colors", type=int, default=64)
    args = parser.parse_args()

    source_path = args.idea_dir / "source" / args.source_name
    source_bytes = source_path.read_bytes()
    with Image.open(source_path) as source:
        image = source.convert("RGB")

    if args.contrast <= 0 or args.saturation <= 0 or args.sharpen < 0 or args.flatten < 0:
        raise ValueError("Contrast and saturation must be positive; sharpen and flatten non-negative")
    if not 2 <= args.colors <= 256:
        raise ValueError("Colors must be between 2 and 256")

    left, top, right, bottom = square_crop(image, args.crop)
    image = image.crop((left, top, right, bottom))

    if args.flatten and args.downsample == "mode":
        image = flatten_texture(image, args.flatten)
    if args.sharpen:
        image = image.filter(
            ImageFilter.UnsharpMask(radius=max(1, image.width // (SIZE * 2)), percent=int(args.sharpen * 100))
        )
    image = ImageEnhance.Color(image).enhance(args.saturation)
    image = ImageEnhance.Contrast(image).enhance(args.contrast)

    if args.downsample == "mode":
        image = downsample_mode(image, WORKING_COLORS)
    else:
        image = image.resize((SIZE, SIZE), Image.Resampling.BOX)

    image = image.quantize(
        colors=args.colors, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE
    ).convert("RGB")

    frame_path = args.idea_dir / "frames" / args.frame
    preview_path = args.idea_dir / "review" / f"{Path(args.frame).stem}-8x.png"
    recipe_path = frame_path.with_suffix(".recipe.json")
    frame_path.parent.mkdir(parents=True, exist_ok=True)
    preview_path.parent.mkdir(parents=True, exist_ok=True)

    image.save(frame_path)
    image.resize((SIZE * PREVIEW_SCALE, SIZE * PREVIEW_SCALE), Image.Resampling.NEAREST).save(preview_path)
    recipe_path.write_text(
        json.dumps(
            {
                "source": str(source_path.relative_to(args.idea_dir)),
                "source_sha256": hashlib.sha256(source_bytes).hexdigest(),
                "crop": [left, top, right, bottom],
                "flatten": args.flatten,
                "sharpen": args.sharpen,
                "saturation": args.saturation,
                "contrast": args.contrast,
                "colors": args.colors,
                "downsample": args.downsample,
                "working_colors": WORKING_COLORS if args.downsample == "mode" else None,
                "quantization": "median_cut_without_dithering",
                "preview_scale": PREVIEW_SCALE,
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    print(f"Frame: {frame_path}\nReview preview: {preview_path}\nRecipe: {recipe_path}")


if __name__ == "__main__":
    main()
