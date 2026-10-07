"""Composite model-drawn run cycles and background plates into a low-FPS 64x64 GIF."""

from pathlib import Path
import math
import subprocess

from PIL import Image, ImageChops, ImageDraw, ImageEnhance, ImageFilter, ImageSequence


ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[1]
FRAME_DIR = ROOT / "animation_frames_v4"
REVIEW_DIR = ROOT / "review"
SIZE = 64
SPLIT_Y = 45          # scenery above the road scrolls; the road and ground stay put
ROAD_Y = (47, 49)
STAR_HOME = (50, 48)
FRAME_MS = 250


def small(name, colors=32):
    with Image.open(ROOT / "source" / f"{name}.png") as image:
        image = ImageEnhance.Contrast(image.convert("RGB")).enhance(1.15)
    image = image.resize((SIZE, SIZE), Image.Resampling.BOX)
    return image.quantize(colors, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE).convert("RGB")


def run_cycle(name):
    """Split a 2x2 magenta-keyed sheet into four 64x64 RGBA runner sprites."""
    with Image.open(ROOT / "source" / f"{name}.png") as sheet:
        sheet = sheet.convert("RGB")
    inset, cell = 6, sheet.width // 2
    sprites = []
    for index in range(4):
        x, y = (index % 2) * cell + inset, (index // 2) * cell + inset
        crop = sheet.crop((x, y, x + cell - 2 * inset, y + cell - 2 * inset))
        pixels = crop.load()
        alpha = Image.new("L", crop.size)
        alpha_pixels = alpha.load()
        for py in range(crop.height):
            for px in range(crop.width):
                r, g, b = pixels[px, py]
                if r - g > 50 and b - g > 50:
                    pixels[px, py] = (10, 10, 14)
                else:
                    alpha_pixels[px, py] = 255
        sprites.append((crop, alpha))
    return sprites


def place_runners(sprites, reference):
    """Scale every pose with the doctor sheet's first pose matched to the approved runner height."""
    top, height = reference
    scale = 36 / height
    size = round(sprites[0][0].width * scale)
    placed = []
    for crop, alpha in sprites:
        crop = ImageEnhance.Contrast(crop).enhance(1.15).resize((size, size), Image.Resampling.BOX)
        crop = crop.quantize(24, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE).convert("RGB")
        alpha = alpha.resize((size, size), Image.Resampling.BOX).point(lambda v: 255 if v >= 128 else 0)
        layer = Image.new("RGBA", (SIZE, SIZE))
        layer.paste(crop, (-round(62 * scale) + 6, 13 - round(top * scale)), alpha)
        placed.append(layer)
    return placed


def milestone(key, plate, box):
    """Cut the object that the key frame has and its runner-free plate lacks."""
    diff = ImageChops.difference(key, plate).convert("L").point(lambda v: 255 if v > 40 else 0)
    mask = Image.new("L", (SIZE, SIZE))
    mask.paste(diff.crop(box), box[:2])
    layer = Image.new("RGBA", (SIZE, SIZE))
    layer.paste(key, (0, 0), mask)
    return layer


def gate_cross():
    """Standing medical cross the star raises on the road: cyan fill with a deep-blue rim."""
    layer = Image.new("RGBA", (14, 16))
    draw = ImageDraw.Draw(layer)
    for grow, color in ((1, (30, 74, 150, 255)), (0, (128, 226, 246, 255))):
        draw.rectangle((5 - grow, 1 - grow, 8 + grow, 14 + grow), fill=color)
        draw.rectangle((1 - grow, 5 - grow, 12 + grow, 8 + grow), fill=color)
    draw.rectangle((5, 5, 8, 8), fill=(220, 252, 255, 255))
    draw.line((6, 2, 6, 4), fill=(206, 248, 255, 255))
    return layer


def gate_palette():
    """Painter's palette with paint dabs and a brush."""
    layer = Image.new("RGBA", (16, 13))
    draw = ImageDraw.Draw(layer)
    draw.ellipse((0, 1, 15, 12), fill=(64, 36, 22, 255))
    draw.ellipse((1, 2, 14, 11), fill=(222, 166, 96, 255))
    draw.ellipse((3, 7, 5, 9), fill=(0, 0, 0, 0))
    for (x, y), color in (((4, 3), (240, 70, 90)), ((7, 3), (255, 206, 60)), ((10, 4), (70, 140, 250)),
                          ((11, 7), (160, 90, 240)), ((8, 8), (60, 210, 160))):
        draw.rectangle((x, y, x + 1, y + 1), fill=color + (255,))
    draw.line((9, 12, 15, 0), fill=(70, 40, 24, 255), width=2)
    draw.rectangle((14, 0, 15, 1), fill=(240, 70, 90, 255))
    return layer


def star_sprite(frame):
    sprite = frame.crop((42, 40, 57, 56))
    mask = Image.new("L", sprite.size)
    ImageDraw.Draw(mask).polygon(
        [(7, 0), (9, 5), (14, 8), (9, 10), (7, 15), (5, 10), (0, 8), (5, 5)], fill=255
    )
    layer = Image.new("RGBA", sprite.size)
    layer.paste(sprite, (0, 0), mask)
    return layer


def gemini_star(radius, center, colors, size=SIZE, curve=0.62):
    """Concave four-point star, |x|^p + |y|^p <= 1, with a diagonal blue-to-violet gradient."""
    layer = Image.new("RGBA", (size, size))
    pixels = layer.load()
    (r0, g0, b0), (r1, g1, b1) = colors
    cx, cy = center
    for y in range(size):
        for x in range(size):
            u, v = (x + 0.5 - cx) / radius, (y + 0.5 - cy) / radius
            if abs(u) ** curve + abs(v) ** curve > 1:
                continue
            t = max(0.0, min(1.0, (u - v + 1.4) / 2.8))
            glow = max(0.0, 1 - math.hypot(u, v) * 2.2) * 0.45
            pixels[x, y] = tuple(
                round(min(255, a + (b - a) * t + (255 - (a + (b - a) * t)) * glow))
                for a, b in ((r0, r1), (g0, g1), (b0, b1))
            ) + (255,)
    return layer


LOGO_COLORS = ((52, 107, 240), (176, 132, 246))
FOUR = [
    "...##.", "..###.", ".####.", "##.##.", "#..##.", "######", "######", "...##.", "...##.",
]
# 7-row pixel glyphs for the wordmark; lowercase letters sit on rows 2-6.
GLYPHS = {
    "G": [".###.", "#...#", "#....", "#.###", "#...#", "#...#", ".###."],
    "e": ["....", "....", ".##.", "#..#", "####", "#...", ".###"],
    "m": [".....", ".....", "##.#.", "#.#.#", "#.#.#", "#.#.#", "#.#.#"],
    "i": ["#", ".", "#", "#", "#", "#", "#"],
    "n": ["....", "....", "###.", "#..#", "#..#", "#..#", "#..#"],
}
WORD = "Gemini"
WORD_SCALE = 2
WORD_ORIGIN = (7, 46)


def word_pixels():
    """Screen pixels of each letter of the wordmark, in reading order."""
    letters, x = [], WORD_ORIGIN[0]
    for char in WORD:
        glyph = GLYPHS[char]
        pixels = []
        for row, line in enumerate(glyph):
            for column, value in enumerate(line):
                if value == "#":
                    for dy in range(WORD_SCALE):
                        for dx in range(WORD_SCALE):
                            pixels.append((x + column * WORD_SCALE + dx, WORD_ORIGIN[1] + row * WORD_SCALE + dy))
        letters.append(pixels)
        x += (len(glyph[0]) + 1) * WORD_SCALE
    return letters


STAR_LOGO_CENTER = (22, 22)


def logo_frame(letters=0, sweep=None):
    """Gemini star with a gray 4; `letters` of the white wordmark appear, `sweep` = x of a passing glint."""
    frame = Image.new("RGB", (SIZE, SIZE), (2, 3, 10))
    draw = ImageDraw.Draw(frame)
    draw.arc((10, -26, 96, 60), 105, 250, fill=(20, 38, 96))
    star = gemini_star(18, STAR_LOGO_CENTER, LOGO_COLORS)
    frame.paste(star, (0, 0), star)
    for row, line in enumerate(FOUR):
        for column, pixel in enumerate(line):
            if pixel == "#":
                draw.rectangle((44 + column * 2, 13 + row * 2, 45 + column * 2, 14 + row * 2), fill=(168, 172, 182))
    for pixels in word_pixels()[:letters]:
        for point in pixels:
            draw.point(point, fill=(240, 243, 250))
    if sweep is not None:
        flare(frame, sweep, 4)
    return frame


class Scene:
    def __init__(self):
        self.plates = [small(f"{p}-plate") for p in ("doctor", "coder", "artist")]
        keys = [small(f"{p}-key") for p in ("doctor", "coder", "artist")]
        self.strips = [self.mirror_strip(plate) for plate in self.plates]
        laptop = milestone(keys[1], self.plates[1], (38, 18, 58, 31))
        self.gates = {"cross": gate_cross(), "laptop": laptop.crop(laptop.getbbox()), "palette": gate_palette()}
        self.star = star_sprite(keys[2])
        reference = run_cycle("doctor-run-sheet")
        top = min(alpha.getbbox()[1] for _, alpha in reference[:1])
        bottom = reference[0][1].getbbox()[3]
        self.runners = {
            name: place_runners(run_cycle(f"{name}-run-sheet"), (top, bottom - top))
            for name in ("hoodie", "doctor", "coder", "artist")
        }

    @staticmethod
    def mirror_strip(plate):
        strip = Image.new("RGB", (SIZE * 2, SIZE))
        strip.paste(plate, (0, 0))
        strip.paste(plate.transpose(Image.Transpose.FLIP_LEFT_RIGHT), (SIZE, 0))
        return strip

    def world(self, stage, scroll, reveal=None):
        """Background for a stage; `reveal` = (next_stage, center, radius) paints the next world in a circle."""
        frame = self.layer(stage, scroll)
        if reveal:
            next_stage, (cx, cy), radius = reveal
            mask = Image.new("L", (SIZE, SIZE))
            draw = ImageDraw.Draw(mask)
            draw.ellipse((cx - radius, cy - radius, cx + radius, cy + radius), fill=255)
            # Paint-like splash: a few satellite drops around the main blob.
            for angle, distance, size in ((0.3, 1.25, 0.32), (1.9, 1.15, 0.26), (3.4, 1.3, 0.22), (4.6, 1.2, 0.3)):
                dx, dy = math.cos(angle) * radius * distance, math.sin(angle) * radius * distance
                r = max(1, radius * size)
                draw.ellipse((cx + dx - r, cy + dy - r, cx + dx + r, cy + dy + r), fill=255)
            frame.paste(self.layer(next_stage, scroll), (0, 0), mask)
        return frame

    def layer(self, stage, scroll):
        frame = self.plates[stage].copy()
        frame.paste(self.strips[stage].crop((scroll, 0, scroll + SIZE, SPLIT_Y)), (0, 0))
        return frame


def speed_marks(frame, scroll, speed):
    draw = ImageDraw.Draw(frame)
    for index in range(2 + speed):
        x = (60 - scroll * 3 - index * 17) % 48
        draw.line((x, 48, x + 1 + speed, 48), fill=(210, 255, 255))
    for index in range(speed):
        y = 30 + index * 4
        x = (40 - scroll * 2 - index * 9) % 30
        draw.line((x, y, x + 2 + speed * 2, y), fill=(236, 240, 246))


def flare(frame, center, size):
    """White four-ray glint: a bright core with rays fading to cyan at the tips."""
    draw = ImageDraw.Draw(frame)
    cx, cy = center
    for step in range(1, size + 1):
        fade = step / (size + 1)
        color = tuple(round(255 - (255 - c) * fade) for c in (150, 230, 255))
        for dx, dy in ((step, 0), (-step, 0), (0, step), (0, -step)):
            draw.point((cx + dx, cy + dy), fill=color)
    if size >= 4:
        for dx, dy in ((1, 1), (-1, 1), (1, -1), (-1, -1)):
            draw.point((cx + dx, cy + dy), fill=(235, 250, 255))
    if size >= 6:
        for dx, dy in ((2, 2), (-2, 2), (2, -2), (-2, -2)):
            draw.point((cx + dx, cy + dy), fill=(170, 225, 250))
    draw.point(center, fill=(255, 255, 255))


def white(layer, color=(255, 255, 255)):
    solid = Image.new("RGBA", layer.size, color + (255,))
    out = Image.new("RGBA", layer.size)
    out.paste(solid, (0, 0), layer.getchannel("A"))
    return out


def shifted(obj, dx):
    layer = Image.new("RGBA", obj.size)
    layer.paste(obj, (-dx, 0))
    return layer


def star_position(tick):
    """The star rides just above the road on a gentle sine."""
    return STAR_HOME[0] + round(math.sin(tick * math.pi / 2 + 1)), STAR_HOME[1] - 1 + round(1.6 * math.sin(tick * math.pi / 2))


def wave_trail(frame, star, tick, amplitude=1.6):
    """Sparkles behind the star trace the same sine it is riding."""
    draw = ImageDraw.Draw(frame)
    for k in range(1, 5):
        x = star[0] - 2 - k * 3
        y = STAR_HOME[1] - 1 + round(amplitude * math.sin(tick * math.pi / 2 - k * 0.9))
        shade = 70 * k // 2
        draw.point((x, y), fill=(max(0, 235 - shade), 255, 255) if k < 3 else (150, 220, 255))


def burst(frame, center, radius):
    """Big white flash: a white core, a pale halo, and four long rays."""
    overlay = Image.new("RGBA", frame.size)
    draw = ImageDraw.Draw(overlay)
    cx, cy = center
    draw.ellipse((cx - radius, cy - radius, cx + radius, cy + radius), fill=(214, 248, 255, 170))
    core = radius * 0.62
    draw.ellipse((cx - core, cy - core, cx + core, cy + core), fill=(255, 255, 255, 255))
    ray = round(radius * 1.7)
    draw.rectangle((cx - ray, cy - 1, cx + ray, cy + 1), fill=(255, 255, 255, 230))
    draw.rectangle((cx - 1, cy - ray, cx + 1, cy + ray), fill=(255, 255, 255, 230))
    frame.paste(overlay, (0, 0), overlay)


def ring(frame, center, radius):
    draw = ImageDraw.Draw(frame)
    cx, cy = center
    draw.ellipse((cx - radius, cy - radius, cx + radius, cy + radius), outline=(255, 255, 255), width=2)
    inner = radius - 3
    draw.ellipse((cx - inner, cy - inner, cx + inner, cy + inner), outline=(190, 240, 255), width=1)


GATE_BASE = 46
CHEST = (20, 28)


def place_gate(frame, sprite, center_x, ghost=False):
    if ghost:
        sprite = white(sprite)
    frame.paste(sprite, (center_x - sprite.width // 2, GATE_BASE - sprite.height), sprite)


def compose(scene, tick, beat):
    stage, scroll, runner_name = beat["stage"], beat["scroll"], beat["runner"]
    star = beat.get("star", star_position(tick))
    frame = scene.world(stage, scroll, beat.get("reveal"))
    speed_marks(frame, scroll, beat["speed"])
    ImageDraw.Draw(frame).rectangle((40, ROAD_Y[0], STAR_HOME[0], ROAD_Y[1]), fill=(0, 238, 252))
    if "gate" in beat:
        name, x, *ghost = beat["gate"]
        place_gate(frame, scene.gates[name], x, bool(ghost))
    runner = scene.runners[runner_name][tick % 4]
    frame.paste(runner, (0, 0), runner)
    if beat.get("trail", True):
        wave_trail(frame, star, tick)
    if beat.get("pulse"):
        flare(frame, star, beat["pulse"])
    frame.paste(scene.star, (star[0] - 7, star[1] - 8), scene.star)
    for center, size in beat.get("flares", ()):
        flare(frame, center, size)
    if "burst" in beat:
        burst(frame, CHEST, beat["burst"])
    if "ring" in beat:
        ring(frame, CHEST, beat["ring"])
    return frame


def flight_path(start, end, steps, height=7):
    """Positions along a rising sine curve from the road toward the viewer."""
    points = []
    for i in range(1, steps + 1):
        t = i / steps
        x = start[0] + (end[0] - start[0]) * t
        y = start[1] + (end[1] - start[1]) * t - height * math.sin(math.pi * t)
        points.append((round(x), round(y)))
    return points


def return_flight(first, home):
    """The star flies back down a sine curve onto the road while the opening scene fades in, closing the loop."""
    frames = []
    path = flight_path(STAR_LOGO_CENTER, home, 3, height=-10)
    for (radius, darkness), center in zip(((12, 0.75), (6, 0.35)), path):
        frame = Image.blend(first, Image.new("RGB", first.size, (2, 3, 10)), darkness)
        star = gemini_star(radius, center, (LOGO_COLORS[0], (0, 238, 252)) if darkness < 0.5 else LOGO_COLORS)
        frame.paste(star, (0, 0), star)
        flare(frame, (center[0] + radius + 2, center[1] - radius // 2), 2)
        frames.append((250, frame))
    return frames


def gate_beats(stage, before, after, gate, scroll, speed, next_stage=None):
    """The star raises a gate on the road, the world carries it to the runner, and he runs through it."""
    spawn = (44, 38)
    beats = [
        (300, dict(stage=stage, scroll=scroll, runner=before, speed=speed, pulse=4, flares=[(spawn, 3)])),
        (350, dict(stage=stage, scroll=scroll + 1, runner=before, speed=speed, gate=(gate, 44, True),
                   flares=[(spawn, 8)])),
        (700, dict(stage=stage, scroll=scroll + 2, runner=before, speed=speed, gate=(gate, 43),
                   flares=[((50, 30), 2)])),
        (250, dict(stage=stage, scroll=scroll + 4, runner=before, speed=speed, gate=(gate, 32))),
        (400, dict(stage=stage, scroll=scroll + 6, runner=before, speed=speed, gate=(gate, 21), burst=22)),
    ]
    reveal = (next_stage, CHEST, 26) if next_stage is not None else None
    beats.append((500, dict(stage=stage, scroll=scroll + 8, runner=after, speed=speed + 1, ring=27, reveal=reveal,
                            flares=[((6, 14), 2), ((36, 10), 3)])))
    return beats


def build():
    scene = Scene()
    timeline = [
        (250, dict(stage=0, scroll=0, runner="hoodie", speed=0)),
        (250, dict(stage=0, scroll=1, runner="hoodie", speed=0)),
    ]
    timeline += gate_beats(0, "hoodie", "doctor", "cross", 2, 1)
    timeline += [(250, dict(stage=0, scroll=11, runner="doctor", speed=2)),
                 (250, dict(stage=0, scroll=13, runner="doctor", speed=2))]
    timeline += gate_beats(0, "doctor", "coder", "laptop", 15, 2, next_stage=1)
    timeline[-1][1]["stage"] = 0
    timeline += [(250, dict(stage=1, scroll=25, runner="coder", speed=3))]
    timeline += gate_beats(1, "coder", "artist", "palette", 28, 3, next_stage=2)
    timeline += [(250, dict(stage=2, scroll=38, runner="artist", speed=4))]

    frames = [(ms, compose(scene, tick, beat)) for tick, (ms, beat) in enumerate(timeline)]
    tick, last = len(timeline), dict(timeline[-1][1], scroll=42)
    path = flight_path((STAR_HOME[0], STAR_HOME[1] - 1), STAR_LOGO_CENTER, 3, height=12)
    frames.append((250, compose(scene, tick, dict(last, star=path[0], trail=False, pulse=3))))
    base = compose(scene, tick + 1, dict(last, star=(-20, -20), trail=False))
    grow = Image.blend(base, Image.new("RGB", base.size, (2, 3, 10)), 0.6)
    star = gemini_star(11, path[1], ((0, 238, 252), LOGO_COLORS[1]))
    grow.paste(star, (0, 0), star)
    frames.append((250, grow))
    letters = word_pixels()
    top_right = max(letters[2], key=lambda p: p[0] - p[1])
    frames.append((600, logo_frame(3, (top_right[0] + 1, top_right[1] - 1))))
    frames.append((3500, logo_frame(6)))
    opening = compose(scene, 0, dict(timeline[0][1], star=(-20, -20), trail=False))
    frames.extend(return_flight(opening, star_position(0)))

    FRAME_DIR.mkdir(exist_ok=True)
    for old in FRAME_DIR.glob("*.png"):
        old.unlink()
    for index, (ms, frame) in enumerate(frames):
        assert frame.size == (SIZE, SIZE)
        frame.save(FRAME_DIR / f"frame_{index:02}_{ms}ms.png")

    columns = 6
    rows = math.ceil(len(frames) / columns)
    sheet = Image.new("RGB", (SIZE * columns, SIZE * rows))
    for index, (_, frame) in enumerate(frames):
        sheet.paste(frame, ((index % columns) * SIZE, (index // columns) * SIZE))
    sheet.resize((sheet.width * 4, sheet.height * 4), Image.Resampling.NEAREST).save(
        REVIEW_DIR / "prototype-v4-contact-sheet.png")
    print(f"Saved {len(frames)} frames")


def enlarge_gif():
    with Image.open(REVIEW_DIR / "prototype-v4.gif") as gif:
        frames, durations = [], []
        for frame in ImageSequence.Iterator(gif):
            durations.append(frame.info["duration"])
            frames.append(frame.convert("RGB").resize((512, 512), Image.Resampling.NEAREST))
    frames[0].save(REVIEW_DIR / "prototype-v4-8x.gif", save_all=True, append_images=frames[1:],
                   duration=durations, loop=0)


if __name__ == "__main__":
    build()
    subprocess.run(
        ["java", "-jar", str(REPO / "artwork-tool/target/artwork-tool-0.1.0-all.jar"),
         "compose", str(FRAME_DIR), str(REVIEW_DIR / "prototype-v4.gif"), str(FRAME_MS)],
        check=True,
    )
    enlarge_gif()
