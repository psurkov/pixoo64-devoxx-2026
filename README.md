# Pixoo 64 artwork for Devoxx Belgium 2026

Source, prompts, and reproducible 64×64 animation exports for the [Google Cloud booth contest](https://devoxx-raffle.cloud.run/).

## Environment

- Java 21 or newer and Maven 3.8 or newer
- Python 3.11 or newer for Nano Banana image generation
- [Jixoo 0.3.0](https://github.com/glaforge/jixoo/tree/v0.3.0), pinned as a Git submodule. It provides the GIF encoder, decoder, and optional Pixoo device CLI. It is not published on Maven Central.

Clone and build:

```sh
git clone --recurse-submodules <this-repository-url>
cd devoxxGoogleCompetition
mvn package -DskipTests
```

For an existing clone: `git submodule update --init --recursive`.

Set up Nano Banana generation through the Google Cloud project with the contest credits:

```sh
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
gcloud auth application-default login
cp .env.example .env
# Edit GOOGLE_CLOUD_PROJECT in .env, then:
source .env
```

The authentication step opens your Google account. Do it only after claiming the contest credits for the intended Cloud project. No API credentials are stored in this repository.

## Artwork workflow

Each concept lives in its own `ideas/<name>/` folder. Its `README.md` describes the proposed image. After the user authorizes one first image, save its English prompt as `prompt.txt` in that folder. The tools keep source images, frames, review previews, and exports beside the idea:

```text
ideas/the-light-on-the-page/
  README.md
  prompt.txt
  source/first.png
  source/first.prompt.txt
  frames/frame_001.png
  frames/frame_001.recipe.json
  review/frame_001-8x.png
  final/entry.gif
```

Generate exactly one square source image after permission:

```sh
.venv/bin/python scripts/generate_image.py ideas/the-light-on-the-page
```

The default model is `gemini-nano-banana-2.1`. The script saves the exact prompt and model next to the source image. A revision uses a new name, for example `--name first-v2`, so the previous source remains available.

Turn the source into the actual 64×64 candidate and an 8× review copy:

```sh
.venv/bin/python scripts/prepare_frame.py ideas/the-light-on-the-page first.png
java -jar artwork-tool/target/artwork-tool-0.1.0-all.jar inspect ideas/the-light-on-the-page/frames/frame_001.png
```

Before preparing a frame, measure how much detail the source actually carries:

```sh
.venv/bin/python scripts/inspect_source.py ideas/the-light-on-the-page/source/first.png
```

A source that reports far more than 64 logical pixels needs a simpler drawing, not a different resize filter. See [docs/pixel-art-for-64x64.md](docs/pixel-art-for-64x64.md).

The frame tool center-crops to a square, flattens fine texture to the locally dominant color, gives each output pixel the color covering most of its cell, and quantizes to 64 colors without dithering. Use `--crop LEFT TOP RIGHT BOTTOM`, `--flatten`, `--sharpen`, `--contrast`, `--saturation`, and `--colors` to tune the result, and `--downsample box` for the older, softer averaging export. It writes the exact settings and source SHA-256 in the frame's recipe file. The review copy is enlarged using nearest-neighbor scaling, so it shows the real pixels without smoothing. **Show both the 64×64 frame and its review copy to the user. Wait for approval before creating other images or a GIF.**

Compose a looping GIF with Jixoo's encoder. The final argument is the default display time per frame in milliseconds; a frame named like `frame_07_600ms.png` uses its own delay instead:

```sh
java -jar artwork-tool/target/artwork-tool-0.1.0-all.jar compose ideas/the-light-on-the-page/frames ideas/the-light-on-the-page/final/entry.gif 100
java -jar artwork-tool/target/artwork-tool-0.1.0-all.jar inspect ideas/the-light-on-the-page/final/entry.gif
```

The tool checks 64×64 dimensions, the contest's 5 MiB file limit, and a maximum of 30 frames. Jixoo's [animation recipes](https://github.com/glaforge/jixoo/blob/v0.3.0/RECIPES.md) warn that Pixoo hardware may loop after about 30–32 frames, so the 30-frame cap keeps the entire animation visible. Use a longer frame delay for a longer loop.

If a Pixoo 64 is available on the local network, display the export with Jixoo's CLI:

```sh
java -jar vendor/jixoo/target/jixoo64-0.3.0-cli.jar -H <device-ip> gif --file ideas/the-light-on-the-page/final/entry.gif
```

The contest accepts up to three square visuals per submission, including PNG and GIF. It does not require exactly 64×64 pixels; we export at native resolution so every submitted pixel maps to one LED. Submission requires a Devoxx conference badge.
