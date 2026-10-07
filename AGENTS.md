# Contest artwork workflow

- Write all repository files, directory names, and image prompts in English. Speak to the user in Russian.
- Brainstorm in text first. Store each distinct idea in its own `ideas/<idea-name>/README.md` file. Describe what the first static 64×64 image would show, why it works, and a possible animation only as a future direction.
- Keep each idea's prompt, generated source, 64×64 frames, review previews, and final exports inside that idea's folder.
- Record manual pixel edits, image revisions, and the user's approval decision in that idea's `README.md`.
- Do not generate an image while discussing ideas. Wait for the user's explicit approval of a specific idea and permission to generate its first frame.
- That permission covers exactly one static image. Prepare its actual 64×64 upload frame and an enlarged preview using nearest-neighbor scaling. Show both to the user and wait for feedback. If changes are requested, revise that image only.
- Generate additional images or animation frames, or assemble a GIF, only after the user explicitly approves the first image and authorizes the next step.
- After animation is authorized, make a low-frame-rate GIF prototype first: a small set of keyframes at about 2–4 fps. Preserve the approved image's art style. Generate only the few new model keyframes needed for changes in character pose or clothing; use code for movement and compositing between them. Show the prototype at 64×64 and enlarged size, record feedback, then refine only as needed.
- Publish the repository or submit artwork to the contest only at the user's explicit request.

## Generate an approved first frame

- Use the repository's Google Cloud generator when the user authorizes a first image. Keep Google credentials in local Application Default Credentials, outside this repository. Never add tokens, credential files, or account secrets to Git.
- Install dependencies with `python3 -m venv .venv` and `.venv/bin/pip install -r requirements.txt` if needed. Sign in locally with `gcloud auth login --update-adc`. Use a billing-enabled project with access to the image model. Copy `.env.example` to the gitignored `.env`, set its project ID, and run `source .env` in the shell used for generation.
- Write the approved idea's English image prompt to `ideas/<name>/prompt.txt`. Run `.venv/bin/python scripts/generate_image.py ideas/<name>` exactly once for the authorized first source. The script writes `source/first.png` and the exact model and prompt to `source/first.prompt.txt`.
- Run `.venv/bin/python scripts/prepare_frame.py ideas/<name> first.png` to make `frames/frame_001.png`, its processing recipe, and `review/frame_001-8x.png`. Inspect the source and both review images. Show the actual 64×64 frame and its nearest-neighbor enlarged preview to the user.
- Record the image path, prompt/model, and pending or received review decision in that idea's `README.md`. When the user requests changes, revise the same first image as a named variant, using `--edit-source first.png --prompt-file prompt-v2.txt --name first-v2` if editing the source with the model. Add `--reference-image references/<file>.png` when an image in the idea folder is a visual reference, and label each input's role in the prompt. Prepare a separate frame and preview for each revision. Extra animation frames or a GIF still need explicit authorization after the first image is approved.
- If the user explicitly requests several fresh starting images, use separate English prompt files and `--prompt-file`/`--name` for each text-to-image candidate. Prepare and show the 64×64 frame and enlarged preview for every candidate. Let the user choose one before developing animation.
