"""Compose model-edited profession keyframes into a low-FPS 64x64 animatic."""

from pathlib import Path
import subprocess

from PIL import Image, ImageDraw, ImageFont, ImageSequence


ROOT = Path(__file__).resolve().parent
SIZE = 64
FRAME_DIR = ROOT / "animation_frames"
REVIEW_DIR = ROOT / "review"
REPO = ROOT.parents[1]
STAR_CENTER = (49, 48)


def artwork(name):
    with Image.open(ROOT / "frames" / f"{name}.png") as image:
        return image.convert("RGB")


def shift_background(image, distance):
    """Move the open scenery on the right while preserving the runner on the left."""
    if not distance:
        return image
    frame = image.copy()
    scenery = image.crop((36, 0, 64, 40))
    offset = distance % scenery.width
    shifted = Image.new("RGB", scenery.size)
    shifted.paste(scenery.crop((offset, 0, scenery.width, 40)), (0, 0))
    shifted.paste(scenery.crop((0, 0, offset, 40)), (scenery.width - offset, 0))
    mask = Image.new("L", scenery.size, 255)
    shade = ImageDraw.Draw(mask)
    for x in range(4):
        shade.line((x, 0, x, 39), fill=x * 64)
    frame.paste(shifted, (36, 0), mask)
    return frame


def clear_old_star(frame):
    """Fill the old star with nearby landscape color before moving its sprite."""
    pixels = frame.load()
    for y in range(40, 56):
        left = pixels[42, y]
        right = pixels[57, y]
        for x in range(43, 57):
            weight = (x - 42) / 15
            pixels[x, y] = tuple(round(a * (1 - weight) + b * weight) for a, b in zip(left, right))


def star_sprite(source):
    sprite = source.crop((42, 40, 57, 56))
    mask = Image.new("L", sprite.size)
    draw = ImageDraw.Draw(mask)
    draw.polygon(
        [(7, 0), (9, 5), (14, 8), (9, 10), (7, 15), (5, 10), (0, 8), (5, 5)],
        fill=255,
    )
    return sprite, mask


def running_frame(base, sprite, mask, star_x, scroll, speed):
    frame = shift_background(base, scroll)
    clear_old_star(frame)
    draw = ImageDraw.Draw(frame)
    draw.rectangle((42, 47, star_x, 49), fill=(27, 193, 231))
    draw.line((42, 47, star_x, 47), fill=(75, 239, 247), width=1)
    frame.paste(sprite, (star_x - 7, STAR_CENTER[1] - 8), mask)
    draw = ImageDraw.Draw(frame)
    for index in range(speed):
        y = 28 + index * 5
        length = 3 + speed + index
        x = (12 - scroll - index * 4) % 19
        draw.line((x - length, y, x, y), fill=(120, 124, 143), width=1)
    return frame


def zoom_frame(square):
    center_x, center_y = 790, 760
    half = square // 2
    with Image.open(ROOT / "source" / "artist-key.png") as high_res:
        image = high_res.convert("RGB")
    crop = image.crop((center_x - half, center_y - half, center_x + half, center_y + half))
    return crop.resize((SIZE, SIZE), Image.Resampling.BOX)


def title_frame():
    frame = Image.new("RGB", (SIZE, SIZE), (5, 12, 39))
    star = zoom_frame(270).resize((34, 34), Image.Resampling.BOX)
    fade = Image.new("L", star.size)
    pixels = fade.load()
    for y in range(34):
        for x in range(34):
            radius = ((x - 16.5) ** 2 + (y - 16.5) ** 2) ** 0.5
            pixels[x, y] = max(0, min(255, round((17 - radius) * 32)))
    frame.paste(star, (15, 1), fade)
    draw = ImageDraw.Draw(frame)
    font = ImageFont.load_default()
    for label, y in (("GEMINI 4", 40), ("ARGON", 50)):
        box = draw.textbbox((0, 0), label, font=font)
        draw.text(((64 - (box[2] - box[0])) // 2, y), label, font=font, fill=(233, 244, 255))
    return frame


def build():
    doctor = artwork("doctor-key")
    coder = artwork("coder-key")
    artist = artwork("artist-key")
    sprite, mask = star_sprite(artist)

    scenes = [
        (doctor, 48, 0, 0),
        (doctor, 49, 1, 1),
        (doctor, 51, 3, 1),
        (Image.blend(doctor, coder, 0.5), 48, 5, 2),
        (coder, 49, 8, 2),
        (coder, 52, 12, 3),
        (Image.blend(coder, artist, 0.5), 49, 17, 3),
        (artist, 50, 23, 4),
        (artist, 53, 30, 5),
        (artist, 56, 38, 5),
    ]
    frames = [running_frame(base, sprite, mask, x, scroll, speed) for base, x, scroll, speed in scenes]
    frames.extend((zoom_frame(520), zoom_frame(270)))
    frames.extend((title_frame(), title_frame()))
    frames.append(frames[0].copy())

    FRAME_DIR.mkdir(exist_ok=True)
    REVIEW_DIR.mkdir(exist_ok=True)
    for index, frame in enumerate(frames):
        frame.save(FRAME_DIR / f"frame_{index:02}.png")

    sheet = Image.new("RGB", (SIZE * 5, SIZE * 3))
    for index, frame in enumerate(frames):
        sheet.paste(frame, ((index % 5) * SIZE, (index // 5) * SIZE))
    sheet.resize((1280, 768), Image.Resampling.NEAREST).save(REVIEW_DIR / "keyframe-contact-sheet.png")
    print(f"Saved {len(frames)} keyframes")


def enlarge_gif():
    with Image.open(REVIEW_DIR / "prototype.gif") as gif:
        frames = [frame.convert("RGB").resize((512, 512), Image.Resampling.NEAREST)
                  for frame in ImageSequence.Iterator(gif)]
        durations = [frame.info.get("duration", 300) for frame in ImageSequence.Iterator(gif)]
    frames[0].save(
        REVIEW_DIR / "prototype-8x.gif", save_all=True, append_images=frames[1:],
        duration=durations, loop=0, optimize=False,
    )


if __name__ == "__main__":
    build()
    subprocess.run(
        [
            "java", "-jar", str(REPO / "artwork-tool/target/artwork-tool-0.1.0-all.jar"),
            "compose", str(FRAME_DIR), str(REVIEW_DIR / "prototype.gif"), "300",
        ],
        check=True,
    )
    enlarge_gif()
