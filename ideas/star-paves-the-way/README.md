# Star Paves the Way

**Status:** The user approved the revised first frame and authorized animation. A low-frame-rate GIF prototype in the approved visual style is ready for review; the prototype itself is not yet approved.

## Core idea

A young man runs toward the right side of the screen. A small four-point Gemini-inspired star flies just ahead of him, continuously drawing the road beneath him. The world begins in black and white. As his run accelerates, he takes on three different professions and the world gains color, until the star flies toward the viewer and becomes the final Gemini 4 Argon reveal.

The star should feel like a companion that opens a way forward. The runner still moves and reaches each milestone himself.

## Proposed first static 64×64 frame

- Show the runner in a clear side silhouette, slightly left of center, with one leg lifted mid-stride. Keep his face and clothing simple enough to read at native size.
- Place the small, bright four-point star near his leading foot. A single continuous luminous road extends backward from the star beneath the runner. Leave the area ahead of the star without a road so its path-building action is understandable.
- Keep the world behind the runner monochrome. Let the fresh tiles and a small area around the star carry the first cyan, blue, and violet colors. The boundary between gray and color should be visible without tiny details.
- Save the milestones for later animation beats. The first frame has only the runner, star, and path as its main shapes.
- No text in this frame. The picture must work as a runner following a star even before the viewer knows the brand reference.

## Possible animation after approval

1. Start in monochrome. The runner wears a doctor's white coat; a large medical cross in the passing scenery helps identify the role at 64×64. The star lights the road ahead.
2. The runner accelerates continuously. The star keeps flying ahead and laying down a path; faster leg motion, quicker background scrolling, and longer color streaks show the rising speed. He never stops to collect anything.
3. Without interrupting his stride, the doctor's coat shifts into a coder's dark-blue hoodie. A large, simple code window passes in the background as cyan spreads through the scene. Then the hoodie shifts into an artist's apron and beret. A brush and broad paint splashes make this final profession recognizable, bringing violet and warm accent colors into the world. These costume and scenery changes are the achievements; no separate reward icons fall from above.
4. At peak speed, the artist's color trail fills the world. The star pulls away, flies toward the viewer, and grows until its four-point silhouette fills the screen.
5. Resolve the large star into the Gemini 4 Argon end mark, then let its light shrink back to the first path tile for a seamless loop. Any wordmark needs a separate 64×64 legibility check; the star must also work on its own.

## Visual constraints

Keep the camera in a side view and the runner at roughly the same screen position while the world scrolls. Use a small number of broad shapes: runner, star, path, and one milestone at a time. The monochrome-to-color change should be the main visual event. At 64×64, the final reveal will need a clean star silhouette and perhaps a separate title beat rather than dense small lettering.

## First-frame review

Review the actual 64×64 frame and its nearest-neighbor enlarged copy together. The frame succeeds if the viewer sees a person running, a star ahead of him, a path forming toward the star, and color starting to spread. If any of those reads only in the enlarged preview, simplify the composition before animation.

### First generated frame

- Prompt: [`prompt.txt`](prompt.txt).
- Model: `gemini-nano-banana-2.1`, recorded with the exact prompt in [`source/first.prompt.txt`](source/first.prompt.txt).
- Generated source: [`source/first.png`](source/first.png).
- Actual 64×64 upload frame: [`frames/frame_001.png`](frames/frame_001.png).
- Nearest-neighbor 8× review preview: [`review/frame_001-8x.png`](review/frame_001-8x.png).
- Processing recipe: [`frames/frame_001.recipe.json`](frames/frame_001.recipe.json).
- Manual pixel edits to the generated still: none. User decision: approved `first-v3.png` for animation.
- Review note: the runner, star, and gray-to-color transition are visible at native size. The original tiles did not clearly show the star building a road, which prompted the continuous-road revisions.

### First-frame revisions

- `first-v2.png`: edit of `first.png` using `prompt-v2.txt`; replaced tiles with a continuous luminous road and lowered the star.
- `first-v3.png`: edit of `first-v2.png` using `prompt-v3.txt`; moved the star closer to the road's leading edge. The model did not materially reduce the runner's size. The user approved this frame to begin animation.
- Approved 64×64 frame: [`frames/frame_001_v3.png`](frames/frame_001_v3.png); preview: [`review/frame_001_v3-8x.png`](review/frame_001_v3-8x.png).
- A code-drawn GIF prototype changed the runner and scenery into much cruder art. The user rejected it and reaffirmed `first-v3.png` as the style reference. That prototype and its renderer were removed. The next prototype will use a small number of model-edited profession and running-pose keyframes instead.

## Low-frame-rate GIF prototype

The user chose three professions: doctor, coder, and artist. Their costumes and scene attributes change while the same person keeps running. Each keyframe was edited from the approved `source/first-v3.png` with `gemini-nano-banana-2.1`; the exact model, edit source, and prompt are saved beside each generated source image.

| Profession | Visual cues | Model keyframe | Prompt |
| --- | --- | --- | --- |
| Doctor | White coat, stethoscope, medical cross | [`source/doctor-key.png`](source/doctor-key.png) | [`prompt-doctor-key.txt`](prompt-doctor-key.txt) |
| Coder | Deep-blue hoodie, headphones, code screen | [`source/coder-key.png`](source/coder-key.png) | [`prompt-coder-key.txt`](prompt-coder-key.txt) |
| Artist | Violet beret, orange apron, brush, paint-colored world | [`source/artist-key.png`](source/artist-key.png) | [`prompt-artist-key.txt`](prompt-artist-key.txt) |

The prepared 64×64 keyframes and their 8× previews are in `frames/` and `review/` with matching profession names. [`build_keyframe_gif.py`](build_keyframe_gif.py) reuses those three frames, shifts the open scenery and star, extends the road, adds speed streaks, zooms into the artist frame's star, and builds the title beat. It uses no image-model calls. Jixoo encodes the 15 keyframes at 300 ms each, about 3.3 fps, for a 4.5-second loop.

- Native review GIF: [`review/prototype.gif`](review/prototype.gif) — 64×64, 15 frames, 39,627 bytes.
- Nearest-neighbor enlarged GIF: [`review/prototype-8x.gif`](review/prototype-8x.gif).
- All-frame contact sheet: [`review/keyframe-contact-sheet.png`](review/keyframe-contact-sheet.png).
- Frame sources: [`animation_frames/`](animation_frames/).
- Rebuild after `mvn package -DskipTests`: `.venv/bin/python ideas/star-paves-the-way/build_keyframe_gif.py`.
- Manual pixel edits: none. Code-driven edits: background scroll, star position, road extension, speed streaks, transition blends, star zoom, and title.
- User decision on this prototype: pending.

## Decisions pending

- Decide whether the final mark needs readable `Gemini 4 Argon` lettering or whether the four-point star plus a short `ARGON` title is enough at 64×64.
- Refine each profession's silhouette after reviewing the low-frame-rate prototype; small costume details may need larger environmental cues at 64×64.

## Running-pose revision (in progress)

The model edits of the full frame kept the runner's pose from `first-v3.png`, so the prototype had no real leg motion. The next prototype separates the character from the world: the model draws run-cycle sprite sheets on a flat magenta key and runner-free background plates; code only keys, scales, and composites them.

- Doctor run cycle: [`prompt-doctor-run-sheet.txt`](prompt-doctor-run-sheet.txt), reference image `source/doctor-key.png`, model `gemini-nano-banana-2.1`, source [`source/doctor-run-sheet.png`](source/doctor-run-sheet.png) (one call).
- [`prepare_run_sheet.py`](prepare_run_sheet.py) splits the 2×2 sheet, keys out magenta (fringe replaced with the outline color), applies 1.15 contrast, box-downsamples the runner to about 36 px tall like the approved frame, and quantizes to 32 colors without dithering. Outputs: `frames/doctor-run-1.png`…`doctor-run-4.png`, [`review/doctor-run-sheet-probe-8x.png`](review/doctor-run-sheet-probe-8x.png), [`review/doctor-run-cycle.gif`](review/doctor-run-cycle.gif), [`review/doctor-run-cycle-8x.gif`](review/doctor-run-cycle-8x.gif).
- Manual pixel edits: none. The user approved the doctor poses and authorized the remaining assets.
- Coder and artist run cycles: edits of `source/doctor-run-sheet.png` with the profession key as costume reference, [`prompt-coder-run-sheet.txt`](prompt-coder-run-sheet.txt), [`prompt-artist-run-sheet.txt`](prompt-artist-run-sheet.txt); sources `source/coder-run-sheet.png`, `source/artist-run-sheet.png`. Poses match the doctor sheet.
- Runner-free background plates: edits of each profession key, [`prompt-doctor-plate.txt`](prompt-doctor-plate.txt), [`prompt-coder-plate.txt`](prompt-coder-plate.txt), [`prompt-artist-plate.txt`](prompt-artist-plate.txt); sources `source/<profession>-plate.png`. Their edges do not tile, so the compositor scrolls each plate joined to its mirror image.

### Prototype v2

[`build_run_gif.py`](build_run_gif.py) composes every frame directly on a 64×64 canvas with no model calls: the four-pose run cycle, scenery above the road scrolling faster each beat, speed marks on the road, and the star cut from the artist key. Milestones are spawned by the star: it rises from the road and traces a cyan medical cross (code-drawn, since the model's gray cross was unreadable), then traces the laptop cut from the coder key, dives into the runner (cyan silhouette flash) and turns him into the coder while cyan spreads from that point; then it sprays the artist world open from the sky before turning him into the artist. At the end the star breaks away, grows over a darkening scene, and becomes the code-drawn Gemini star with a pixel `4` on black (no text). A last frame shrinks the star onto the road to loop.

- Native GIF: [`review/prototype-v2.gif`](review/prototype-v2.gif) — 64×64, 26 frames at 250 ms (4 fps), 6.5 s.
- Enlarged GIF: [`review/prototype-v2-8x.gif`](review/prototype-v2-8x.gif); contact sheet: [`review/prototype-v2-contact-sheet.png`](review/prototype-v2-contact-sheet.png); frames: `animation_frames_v2/`.
- Rebuild: `arch -arm64 .venv/bin/python ideas/star-paves-the-way/build_run_gif.py` (the venv is arm64).
- Manual pixel edits: none. User decision on prototype v2: pending.

### User feedback on the previous prototype

- The star should visibly help create each milestone (it spawns the medical cross, code screen, and paint), rather than the milestones simply drifting into view.
- Every frame, including the ending, must be a true 64×64 image.
- Drop the `GEMINI 4 / ARGON` text ending. End with a large `4` and the Gemini four-point star logo. Logo reference: [`references/gemini-4-argon-logo.png`](references/gemini-4-argon-logo.png) (blue-to-violet star on black).

### Prototype v3

User feedback on v2: much better. Requested changes: the star should move smoothly on a sine instead of straight lines; milestones should appear through a white glint; the star must stay on the road while spawning (only the finale flies away); the finale should show the `Gemini` word appearing below the star.

- The star now rides the road's end on a gentle sine (±2 px) with sparkles tracing that wave behind it. It never leaves the road until the finale.
- Each milestone spawns in three beats while the star flares on the road: a small white glint, a large glint over the object's white silhouette, then the object with a leftover sparkle. Profession changes use a white runner silhouette. The coder's cyan spreads from the star; the artist's colors burst from a sky glint as a splash-shaped reveal.
- Finale: the star leaves the road along a rising sine curve, grows as the scene darkens, and becomes the Gemini star with a gray `4`. A hand-built 2× pixel font writes `Gemini` below in three steps, a glint riding the newest letter.
- Native GIF: [`review/prototype-v3.gif`](review/prototype-v3.gif) — 64×64, 28 frames at 250 ms, 7 s, 58 KB. Enlarged: [`review/prototype-v3-8x.gif`](review/prototype-v3-8x.gif); contact sheet: [`review/prototype-v3-contact-sheet.png`](review/prototype-v3-contact-sheet.png); frames: `animation_frames_v3/`.
- No new model calls. Manual pixel edits: none. User decision on prototype v3: pending.

### Prototype v4

User feedback on v3: good overall, but it was unclear that the star helps him reach each achievement. Asked for more pauses between events and a bigger white flash. The user approved the "gate" story below, one more model call, and per-frame delays in `artwork-tool`.

- New asset: hoodie run cycle, edit of `source/doctor-run-sheet.png` with `source/first-v3.png` as costume reference, [`prompt-hoodie-run-sheet.txt`](prompt-hoodie-run-sheet.txt), source `source/hoodie-run-sheet.png` (one call). The run now starts with the ordinary runner from the approved frame.
- Story per profession: the star flares on the road, a white glint grows into the gate's white silhouette, and the gate stands on the road (held 450 ms). The scrolling world carries it to the runner; he runs through it in a large white burst, then steps out in the new outfit inside an expanding white ring that also reveals the next world's color. Gates: code-drawn cyan medical cross, the laptop cut from the coder key, a code-drawn painter's palette. Plain running beats separate the events.
- Finale: the star leaves on a sine curve and grows over a darkening scene, then the Gemini star and gray `4`, the `Gemini` word in two steps, and a 1.8 s hold.
- Loop (user request after v4 approval: "super"): the logo star flies back down a sine curve and shrinks onto the road while the opening scene fades in from black, so the last frame flows into the first. To stay within 30 frames, the separate star-and-`4` frame was dropped; `Gem` now appears with the logo (450 ms), then the full word (1.8 s).
- Frames are named `frame_NN_<ms>ms.png`; `artwork-tool compose` reads each frame's delay from that suffix.
- Native GIF: [`review/prototype-v4.gif`](review/prototype-v4.gif) — 64×64, 30 frames (the cap), 14.1 s, 68 KB. Enlarged: [`review/prototype-v4-8x.gif`](review/prototype-v4-8x.gif); contact sheet: [`review/prototype-v4-contact-sheet.png`](review/prototype-v4-contact-sheet.png); frames: `animation_frames_v4/`.
- Manual pixel edits: none. User decision on prototype v4: pending.
- Longer cut (user request): the 30-frame cap stays because Pixoo may loop early beyond it, so the GIF is lengthened through delays only. Running frames remain 250 ms. Per gate: star flare 300 ms, white glint 350 ms, standing gate 700 ms, burst 400 ms, ring 500 ms. `Gem` 600 ms; the complete logo with `Gemini` holds 3.5 s. Total 14.1 s.
