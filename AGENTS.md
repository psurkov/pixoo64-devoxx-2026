# Contest artwork workflow

- Write all repository files, directory names, and image prompts in English. Speak to the user in Russian.
- Brainstorm in text first. Store each distinct idea in its own `ideas/<idea-name>/README.md` file. Describe what the first static 64×64 image would show, why it works, and a possible animation only as a future direction.
- Keep each idea's prompt, generated source, 64×64 frames, review previews, and final exports inside that idea's folder.
- Record manual pixel edits, image revisions, and the user's approval decision in that idea's `README.md`.
- Do not generate an image while discussing ideas. Wait for the user's explicit approval of a specific idea and permission to generate its first frame.
- That permission covers exactly one static image. Prepare its actual 64×64 upload frame and an enlarged preview using nearest-neighbor scaling. Show both to the user and wait for feedback. If changes are requested, revise that image only.
- Generate additional images or animation frames, or assemble a GIF, only after the user explicitly approves the first image and authorizes the next step.
- Publish the repository or submit artwork to the contest only at the user's explicit request.
