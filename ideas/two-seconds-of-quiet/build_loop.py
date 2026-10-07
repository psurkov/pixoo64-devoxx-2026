"""Draw the coffee steam for the quiet loop, and preview it on the still frame.

The steam is code, not a generation: it is the motion of this piece, and at 64x64 it is a handful
of single pixels, which the model cannot place or hold steady between frames.
"""

import argparse
import math
from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parent
SIZE = 64
PREVIEW_SCALE = 8
LOOP_FRAMES = 30

STEAM = (244, 232, 214)
PUFFS = 6
# Measured on frame_001_v2: the ceramic rim sits at rows 37-38 and the coffee at rows 39-41. The
# page fills the space straight above, so the wisp leans right into the clear wood at x 54..60.
MUG_MOUTH = (55, 36)
STEAM_TOP = 26


def steam_trail(phase: float) -> list[tuple[int, int, float]]:
    """One wisp drifting up and fading, as (x, y, strength).

    `phase` runs 0..1 over the loop. Each puff keeps its own offset in that cycle, so the trail
    returns to its own start and the loop closes without a jump.
    """
    mouth_x, mouth_y = MUG_MOUTH
    height = mouth_y - STEAM_TOP
    puffs = []
    for index in range(PUFFS):
        travel = (phase + index / PUFFS) % 1.0
        y = mouth_y - round(travel * height)
        # Lean steadily right, away from the bright page, with a slow waver on top of the drift.
        sway = round(travel * 3.0 + 0.9 * math.sin(travel * 2 * math.pi))
        strength = (1.0 - travel * 0.75) * 0.95
        puffs.append((mouth_x + sway, y, strength))
        if travel < 0.35:
            puffs.append((mouth_x + sway + 1, y, strength * 0.6))
    return puffs


def with_steam(image: Image.Image, phase: float) -> Image.Image:
    image = image.copy()
    for x, y, strength in steam_trail(phase):
        if not (0 <= x < SIZE and STEAM_TOP <= y < SIZE):
            continue
        base = image.getpixel((x, y))
        blended = tuple(round(a + (b - a) * strength) for a, b in zip(base, STEAM))
        ImageDraw.Draw(image).point((x, y), fill=blended)
    return image


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--frame", default="frame_001_v2.png")
    parser.add_argument("--name", default="frame_001_v3")
    parser.add_argument("--phase", type=float, default=0.0)
    args = parser.parse_args()

    with Image.open(ROOT / "frames" / args.frame) as opened:
        still = with_steam(opened.convert("RGB"), args.phase)
    still.save(ROOT / "frames" / f"{args.name}.png")
    still.resize((SIZE * PREVIEW_SCALE, SIZE * PREVIEW_SCALE), Image.Resampling.NEAREST).save(
        ROOT / "review" / f"{args.name}-8x.png"
    )

    strip = Image.new("RGB", (SIZE * 6, SIZE))
    for column in range(6):
        strip.paste(with_steam(still, column / 6), (column * SIZE, 0))
    strip.resize((SIZE * 6 * 5, SIZE * 5), Image.Resampling.NEAREST).save(
        ROOT / "review" / f"{args.name}-steam-phases.png"
    )
    print(f"Frame: frames/{args.name}.png\nPreview: review/{args.name}-8x.png")


if __name__ == "__main__":
    main()


# --- the loop ------------------------------------------------------------------------------------
# Every cycle length divides LOOP_FRAMES, so each one returns to its own start and the loop closes
# without a stutter at the seam.
CAT_RECT = (30, 12, 53, 22)
EAR_RECT = (31, 12, 37, 16)
WINDOW_GROUPS = (
    (((56, 5), (56, 6), (58, 5), (58, 6), (59, 6)), 15),
    (((56, 13), (56, 14), (58, 13), (58, 14)), 10),
    (((38, 5), (41, 5), (38, 13), (39, 11)), 30),
)
FRAME_MS = 70


def lift(image: Image.Image, rect: tuple[int, int, int, int]) -> Image.Image:
    """Raise one block by a single pixel and refill the row it leaves behind.

    One pixel is the whole range of motion available here: at 64x64 anything larger stops reading
    as breathing and starts reading as a jump.
    """
    left, top, right, bottom = rect
    image = image.copy()
    block = image.crop(rect)
    image.paste(block, (left, top - 1))
    image.paste(image.crop((left, bottom - 2, right, bottom - 1)), (left, bottom - 1))
    return image


def flicker(image: Image.Image, phase: float) -> Image.Image:
    """Breathe the lit windows of the city, each group on its own cycle."""
    image = image.copy()
    draw = ImageDraw.Draw(image)
    for points, period in WINDOW_GROUPS:
        turn = (phase * LOOP_FRAMES / period) % 1.0
        level = 0.72 + 0.28 * math.cos(turn * 2 * math.pi)
        for x, y in points:
            red, green, blue = image.getpixel((x, y))
            draw.point((x, y), fill=(round(red * level), round(green * level), round(blue * level)))
    return image


def loop_frame(plate: Image.Image, index: int) -> Image.Image:
    phase = index / LOOP_FRAMES
    image = plate
    if math.sin(phase * 2 * math.pi) > 0.5:
        image = lift(image, CAT_RECT)
    if index in (13, 14):
        image = lift(image, EAR_RECT)
    image = flicker(image, phase)
    return with_steam(image, phase)


def build_loop() -> None:
    import subprocess

    with Image.open(ROOT / "frames" / "frame_001_v2.png") as opened:
        plate = with_text(opened.convert("RGB"))
    plate.save(ROOT / "frames" / "frame_001_v4.png")
    plate.resize((SIZE * PREVIEW_SCALE, SIZE * PREVIEW_SCALE), Image.Resampling.NEAREST).save(
        ROOT / "review" / "frame_001_v4-8x.png"
    )
    frame_dir = ROOT / "animation_frames"
    frame_dir.mkdir(exist_ok=True)
    for existing in frame_dir.glob("frame_*.png"):
        existing.unlink()

    frames = [loop_frame(plate, index) for index in range(LOOP_FRAMES)]
    for index, image in enumerate(frames):
        image.save(frame_dir / f"frame_{index:02}.png")

    jar = ROOT.parents[1] / "artwork-tool/target/artwork-tool-0.1.0-all.jar"
    gif = ROOT / "review" / "prototype.gif"
    subprocess.run(["java", "-jar", str(jar), "compose", str(frame_dir), str(gif),
                    str(FRAME_MS)], check=True)

    from PIL import ImageSequence
    with Image.open(gif) as opened:
        large = [image.convert("RGB").resize((512, 512), Image.Resampling.NEAREST)
                 for image in ImageSequence.Iterator(opened)]
    large[0].save(ROOT / "review" / "prototype-8x.gif", save_all=True, append_images=large[1:],
                  duration=FRAME_MS, loop=0, optimize=False)

    sheet = Image.new("RGB", (SIZE * 6, SIZE * 5))
    for index, image in enumerate(frames):
        sheet.paste(image, ((index % 6) * SIZE, (index // 6) * SIZE))
    sheet.resize((SIZE * 6 * 4, SIZE * 5 * 4), Image.Resampling.NEAREST).save(
        ROOT / "review" / "prototype-contact-sheet.png"
    )
    print(f"Saved {len(frames)} frames at {FRAME_MS} ms each")


# --- text on the pages ---------------------------------------------------------------------------
TEXT_INK = (150, 124, 110)
BOOK_BOX = (16, 22, 50, 46)
SPINE = (32, 35)
# Lines sit at these fractions of the way down the page, and their lengths vary from a fixed
# pattern so the rows read as text rather than as a ruled grid.
TEXT_DEPTHS = (0.16, 0.31, 0.46, 0.61, 0.76)
LINE_TRIM = (1, 2, 1, 4, 1, 2, 5, 1, 3, 1)


def page_edges(image: Image.Image) -> dict[int, tuple[int, int]]:
    """For each column of the book, the top and bottom row of open page.

    The pages are a wedge in perspective - their top edge and bottom edge run at different angles -
    so a line of text can only look right if it is placed relative to both.
    """
    left, top, right, bottom = BOOK_BOX
    edges = {}
    for x in range(left, right + 1):
        rows = [
            y for y in range(top, bottom + 1)
            if sum(channel * weight for channel, weight
                   in zip(image.getpixel((x, y)), (0.299, 0.587, 0.114))) > 205
        ]
        if len(rows) >= 8:
            edges[x] = (rows[0], rows[-1])
    return edges


def with_text(image: Image.Image) -> Image.Image:
    """Set lines of text across both pages, each line following the page's own perspective.

    A line runs at a constant fraction of the way down the page rather than along a constant row,
    so it leans with the page instead of cutting across it.
    """
    image = image.copy()
    draw = ImageDraw.Draw(image)
    edges = page_edges(image)
    pages = (
        [x for x in sorted(edges) if x <= SPINE[0]],
        [x for x in sorted(edges) if x >= SPINE[1]],
    )
    index = 0
    for depth in TEXT_DEPTHS:
        for page in pages:
            if len(page) < 6:
                continue
            trim = LINE_TRIM[index % len(LINE_TRIM)]
            index += 1
            run = page[1:max(len(page) - trim, 4)]
            points = [
                (x, round(edges[x][0] + (edges[x][1] - edges[x][0]) * depth)) for x in run
            ]
            if len(points) >= 4:
                draw.line(points, fill=TEXT_INK)
    return image
