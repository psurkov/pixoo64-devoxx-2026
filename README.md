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

Save source images in `artwork/source/`, the final 64×64 PNG frames in `artwork/frames/` with zero-padded names such as `frame_001.png`, and contest exports in `artwork/final/`. Record generation prompts and settings in `prompts/`.

Generate a square source PNG from a saved prompt:

```sh
.venv/bin/python scripts/generate_image.py prompts/entry.txt artwork/source/entry.png
```

The default model is `gemini-nano-banana-2.1`. Review and approve the first static image before generating more images or animation, as described in `AGENTS.md`. The source PNG then needs deliberate 64×64 pixel editing before it becomes a final frame.

Compose a looping GIF with Jixoo's encoder. The final argument is each frame's display time in milliseconds:

```sh
java -jar artwork-tool/target/artwork-tool-0.1.0-all.jar compose artwork/frames artwork/final/entry.gif 100
java -jar artwork-tool/target/artwork-tool-0.1.0-all.jar inspect artwork/final/entry.gif
```

The tool checks 64×64 dimensions, the contest's 5 MiB file limit, and a maximum of 30 frames. Jixoo's [animation recipes](https://github.com/glaforge/jixoo/blob/v0.3.0/RECIPES.md) warn that Pixoo hardware may loop after about 30–32 frames, so the 30-frame cap keeps the entire animation visible. Use a longer frame delay for a longer loop.

If a Pixoo 64 is available on the local network, display the export with Jixoo's CLI:

```sh
java -jar vendor/jixoo/target/jixoo64-0.3.0-cli.jar -H <device-ip> gif --file artwork/final/entry.gif
```

The contest accepts up to three square visuals per submission, including PNG and GIF. It does not require exactly 64×64 pixels; we export at native resolution so every submitted pixel maps to one LED. Submission requires a Devoxx conference badge. No artwork has been generated or submitted yet.
