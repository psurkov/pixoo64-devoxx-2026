"""Compose the approved lamp frame into a low-FPS 64x64 animatic.

The room and the drawing come from the model; the lighting, the lamp zoom, the argon reveal and the
Gemini star are composited in code. Only the paper region of each drawing keyframe is pasted onto
the approved plate, so the hair, cat, window, mug and lamp cannot drift between frames.
"""

from pathlib import Path
import subprocess
import sys

from PIL import Image, ImageDraw, ImageFilter, ImageSequence

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[1]
sys.path.insert(0, str(REPO / "scripts"))
from prepare_frame import downsample_mode, flatten_texture  # noqa: E402

SIZE = 64
FRAME_DIR = ROOT / "animation_frames"
REVIEW_DIR = ROOT / "review"
FRAME_MS = 300
WORKING_COLORS = 48

NIGHT = (4, 9, 24)
ARGON = (190, 234, 255)
STAR_TOP = (53, 99, 244)
STAR_BOTTOM = (152, 135, 244)
HELPER_VIOLET = (150, 120, 246)

PLATE = "frame_user-grid-v7"
DRAWING_STEPS = ("frame_step-a", "frame_step-b-v2", "frame_step-c-v2")
SOURCE_IMAGE = "user-grid-v7.png"

BULB_CENTER = (54, 42)
BULB_RADIUS = 7
GLOW_RADIUS = 12
CENTER = (32, 32)
# The same bulb, measured on the 1024-pixel source the plate was reduced from.
SOURCE_SIDE = 1024
BULB_SOURCE = (872, 672)
BULB_SOURCE_RADIUS = 112


def frame(name: str) -> Image.Image:
    with Image.open(ROOT / "frames" / f"{name}.png") as image:
        return image.convert("RGB")


def paper_region() -> Image.Image:
    """The part of the plate the model's drawing keyframes are allowed to replace.

    It is the sheet itself, grown by two pixels so a moving hand and the protractor can cross its
    edge, plus the strip of desk where the protractor lands - and never the bulb or its halo.
    """
    plate = frame(PLATE)
    pixels = plate.load()
    sheet = Image.new("L", (SIZE, SIZE))
    sheet_pixels = sheet.load()
    for y in range(SIZE):
        for x in range(SIZE):
            red, green, blue = pixels[x, y]
            luma = 0.299 * red + 0.587 * green + 0.114 * blue
            sheet_pixels[x, y] = 255 if luma > 195 and blue > 165 else 0
    region = sheet.filter(ImageFilter.MaxFilter(5))

    draw = ImageDraw.Draw(region)
    draw.rectangle((40, 46, 58, 58), fill=255)
    for corner in ((14, 18, 56, 58),):
        outside = Image.new("L", (SIZE, SIZE))
        ImageDraw.Draw(outside).rectangle(corner, fill=255)
        region = Image.composite(region, Image.new("L", (SIZE, SIZE)), outside)
    x, y = BULB_CENTER
    ImageDraw.Draw(region).ellipse(
        (x - GLOW_RADIUS, y - GLOW_RADIUS, x + GLOW_RADIUS, y + GLOW_RADIUS), fill=0
    )
    return region


def lamp_mask(glow: float = 1.0) -> Image.Image:
    """Keep the bulb lit while the room around it falls into shadow."""
    mask = Image.new("L", (SIZE, SIZE))
    draw = ImageDraw.Draw(mask)
    x, y = BULB_CENTER
    draw.ellipse((x - GLOW_RADIUS, y - GLOW_RADIUS, x + GLOW_RADIUS, y + GLOW_RADIUS),
                 fill=round(140 * glow))
    draw.ellipse((x - BULB_RADIUS, y - BULB_RADIUS, x + BULB_RADIUS, y + BULB_RADIUS),
                 fill=round(255 * glow))
    return mask


def dim(image: Image.Image, level: float, glow: float = 1.0) -> Image.Image:
    """Sink the room toward night blue, holding the bulb at its own brightness."""
    night = Image.new("RGB", (SIZE, SIZE), NIGHT)
    return Image.composite(image, Image.blend(night, image, level), lamp_mask(glow))


def helping(image: Image.Image, amount: float) -> Image.Image:
    """Flick the bulb violet, so the lamp reads as helping while she draws."""
    violet = Image.new("RGB", (SIZE, SIZE), HELPER_VIOLET)
    tinted = Image.blend(image, violet, amount)
    return Image.composite(tinted, image, lamp_mask())


def zoom(crop_side: int) -> tuple[Image.Image, tuple[float, float], float]:
    """Push in on the bulb from the full-resolution source, not onto a redrawn one.

    Returns the frame plus where the glass ended up, so the lettering can be placed inside it.
    """
    with Image.open(ROOT / "source" / SOURCE_IMAGE) as opened:
        source = opened.convert("RGB").resize((SOURCE_SIDE, SOURCE_SIDE), Image.Resampling.LANCZOS)

    progress = (SOURCE_SIDE - crop_side) / (SOURCE_SIDE - 330)
    center_x = SOURCE_SIDE / 2 + (BULB_SOURCE[0] - SOURCE_SIDE / 2) * progress
    center_y = SOURCE_SIDE / 2 + (BULB_SOURCE[1] - SOURCE_SIDE / 2) * progress
    left = min(max(center_x - crop_side / 2, 0), SOURCE_SIDE - crop_side)
    top = min(max(center_y - crop_side / 2, 0), SOURCE_SIDE - crop_side)

    crop = source.crop((round(left), round(top), round(left) + crop_side, round(top) + crop_side))
    crop = flatten_texture(crop, 0.55)
    image = downsample_mode(crop, WORKING_COLORS)

    scale = SIZE / crop_side
    glass = ((BULB_SOURCE[0] - left) * scale, (BULB_SOURCE[1] - top) * scale)
    return image, glass, BULB_SOURCE_RADIUS * scale


def shade_around(image: Image.Image, center: tuple[float, float], radius: float,
                 level: float) -> Image.Image:
    """Hold a lit disc and let the rest of the zoomed frame fall away into night."""
    mask = Image.new("L", (SIZE, SIZE))
    draw = ImageDraw.Draw(mask)
    x, y = center
    draw.ellipse((x - radius * 1.5, y - radius * 1.5, x + radius * 1.5, y + radius * 1.5), fill=120)
    draw.ellipse((x - radius, y - radius, x + radius, y + radius), fill=255)
    night = Image.new("RGB", (SIZE, SIZE), NIGHT)
    return Image.composite(image, Image.blend(night, image, level), mask)


def argon_letters(image: Image.Image, center: tuple[float, float], radius: float,
                  fade: float = 1.0) -> Image.Image:
    """Spell `Ar` inside the glass, by hand: the only lettering in the loop."""
    image = image.copy()
    layer = image.copy()
    draw = ImageDraw.Draw(layer)
    x, y = center
    height = radius * 0.85
    width = max(2, round(radius * 0.09))
    draw.line((x - radius * 0.62, y + height * 0.5, x - radius * 0.26, y - height * 0.55),
              fill=ARGON, width=width)
    draw.line((x - radius * 0.26, y - height * 0.55, x + radius * 0.10, y + height * 0.5),
              fill=ARGON, width=width)
    draw.line((x - radius * 0.46, y + height * 0.08, x - radius * 0.06, y + height * 0.08),
              fill=ARGON, width=width)
    draw.line((x + radius * 0.34, y - height * 0.12, x + radius * 0.34, y + height * 0.5),
              fill=ARGON, width=width)
    draw.line((x + radius * 0.34, y - height * 0.02, x + radius * 0.64, y - height * 0.18),
              fill=ARGON, width=width)
    return Image.blend(image, layer, fade)


def tint_glass(image: Image.Image, center: tuple[float, float], radius: float,
               amount: float) -> Image.Image:
    """Turn the glass from amber to the star's blue-violet before it becomes the star."""
    mask = Image.new("L", (SIZE, SIZE))
    x, y = center
    ImageDraw.Draw(mask).ellipse((x - radius, y - radius, x + radius, y + radius), fill=255)
    violet = Image.new("RGB", (SIZE, SIZE), STAR_BOTTOM)
    return Image.composite(Image.blend(image, violet, amount), image, mask)


def star_frame(radius: int, brightness: float) -> Image.Image:
    """One four-point star, tapered, on a dark field."""
    image = Image.new("RGB", (SIZE, SIZE), NIGHT)
    gradient = Image.new("RGB", (SIZE, SIZE))
    pixels = gradient.load()
    for y in range(SIZE):
        weight = y / (SIZE - 1)
        color = tuple(
            round((a + (b - a) * weight) * brightness) for a, b in zip(STAR_TOP, STAR_BOTTOM)
        )
        for x in range(SIZE):
            pixels[x, y] = color

    mask = Image.new("L", (SIZE, SIZE))
    draw = ImageDraw.Draw(mask)
    x, y = CENTER
    waist = max(2, round(radius * 0.28))
    draw.polygon(
        [
            (x, y - radius), (x + waist, y - waist), (x + radius, y), (x + waist, y + waist),
            (x, y + radius), (x - waist, y + waist), (x - radius, y), (x - waist, y - waist),
        ],
        fill=255,
    )
    image.paste(gradient, (0, 0), mask)
    return image


def build() -> list[Image.Image]:
    plate = frame(PLATE)
    region = paper_region()
    steps = [Image.composite(frame(name), plate, region) for name in DRAWING_STEPS]
    finished = steps[-1]

    frames = [dim(plate, 0.10, glow=0.15), dim(plate, 0.45, glow=0.70), plate]
    for step in steps:
        frames.append(step)
        frames.append(helping(step, 0.45))
    frames.append(finished)
    frames.append(dim(finished, 0.40))
    frames.append(dim(finished, 0.14))

    for crop_side in (820, 620, 460, 330):
        image, glass, radius = zoom(crop_side)
        frames.append(shade_around(image, glass, radius * 1.3, 0.10))

    image, glass, radius = zoom(330)
    lit = shade_around(image, glass, radius * 1.3, 0.06)
    frames.append(argon_letters(lit, glass, radius, fade=0.55))
    frames.append(argon_letters(lit, glass, radius))
    frames.append(argon_letters(tint_glass(lit, glass, radius, 0.5), glass, radius, fade=0.7))
    frames.append(tint_glass(lit, glass, radius, 0.9))

    frames += [star_frame(16, 1.0), star_frame(25, 1.0), star_frame(27, 0.5)]
    frames.append(dim(plate, 0.08, glow=0.12))
    return frames


def save(frames: list[Image.Image]) -> None:
    FRAME_DIR.mkdir(exist_ok=True)
    REVIEW_DIR.mkdir(exist_ok=True)
    for existing in FRAME_DIR.glob("frame_*.png"):
        existing.unlink()
    for index, image in enumerate(frames):
        image.save(FRAME_DIR / f"frame_{index:02}.png")

    columns = 6
    rows = (len(frames) + columns - 1) // columns
    sheet = Image.new("RGB", (SIZE * columns, SIZE * rows), NIGHT)
    for index, image in enumerate(frames):
        sheet.paste(image, ((index % columns) * SIZE, (index // columns) * SIZE))
    sheet.resize((SIZE * columns * 4, SIZE * rows * 4), Image.Resampling.NEAREST).save(
        REVIEW_DIR / "prototype-contact-sheet.png"
    )
    print(f"Saved {len(frames)} frames at {FRAME_MS} ms each")


def enlarge_gif() -> None:
    with Image.open(REVIEW_DIR / "prototype.gif") as gif:
        frames = [
            image.convert("RGB").resize((512, 512), Image.Resampling.NEAREST)
            for image in ImageSequence.Iterator(gif)
        ]
    frames[0].save(
        REVIEW_DIR / "prototype-8x.gif", save_all=True, append_images=frames[1:],
        duration=FRAME_MS, loop=0, optimize=False,
    )


if __name__ == "__main__":
    save(build())
    subprocess.run(
        [
            "java", "-jar", str(REPO / "artwork-tool/target/artwork-tool-0.1.0-all.jar"),
            "compose", str(FRAME_DIR), str(REVIEW_DIR / "prototype.gif"), str(FRAME_MS),
        ],
        check=True,
    )
    enlarge_gif()
