# The Light on the Page

**Status:** the user selected a supplied lo-fi base image and the enlarged-lamp layout. `user-grid-v5.png` fixed readability at native size but its colors collapsed into one amber-brown tone; `user-grid-v7.png` is the approved first frame. The user then authorized animation, and a low-frame-rate prototype is awaiting review.

## Core scene

A quiet, cozy, lo-fi engineering desk. A young woman sits beside a glowing freestanding desk bulb, with a pencil poised over a clean sheet. A coffee mug, a sleeping orange cat on the window ledge, and a couple of plants make the room feel lived in. During a future animation, she draws a simple technical diagram in the warm pool of light.

Argon is used inside incandescent bulbs to protect the filament. The glowing filament provides the light. The physical argon in the lamp creates a visual bridge to the name Gemini 4 Argon. The scene should first read as a person absorbed in engineering work, then reveal that connection at the end.

## Proposed first static 64×64 frame

- Fixed, high diagonal view of the user-supplied room. The woman sits at left with a large blank sheet in front of her; a prominent freestanding incandescent bulb stands on the wooden tabletop in the lower-right foreground.
- The bulb has just turned on. Its clear rounded glass and amber glow remain visible at 64×64. A visible filament line is acceptable. Amber light reaches the paper and hand; their distinct colors keep the drawing gesture legible.
- The sheet is completely blank. She holds a pencil just above it, ready to draw.
- A small coffee mug sits farther back at right. An orange cat curls up above the paper. The blue night city through the window uses a few large silhouettes and lit squares, so the woman, sheet, bulb, mug and cat remain readable at native size. No ruler or tiny writing.

## Color direction

Use the Gemini 4 Argon artwork supplied as a color reference: deep navy (`#071233`), dark blue (`#123068`), clear blue (`#3B84E2`), pale cyan (`#BEEAFF`), and white. The supplied four-point Gemini star adds a brighter blue (`#3563F4`) to soft violet (`#9887F4`) gradient against near-black navy (`#040918`). These are approximate samples from the images, not a formal brand palette.

The selected room uses reddish-brown wood and burgundy clothing against a dark-blue night city, with an orange cat and a large golden bulb. The incandescent lamp adds an amber pool over warm cream paper. As the scene shifts to the model reveal, the amber gives way to the star's blue-violet gradient. Keep the window simple and use large shapes and strong value contrast so the woman, lamp and blank page read at 64×64 without zooming.

## Possible animation after approval

1. Begin in near darkness. The lamp turns on and reveals the engineer, pencil, and mostly blank sheet: the starting scene described above.
2. The hand moves with the pencil as a clear technical diagram grows on the paper. Use a few larger geometric marks rather than dense text so the act of drawing remains visible at 64×64.
3. The desk and paper fade into navy shadow while the lamp keeps shining in the same position. A small pale-blue `Ar` appears inside the bulb as a graphic clue to the argon within it.
4. The lamp's glow turns blue and resolves into one large four-point Gemini star on a dark field. Give its tapered points and blue-to-violet color enough space to read at 64×64. The star fades into darkness; the warm lamp switches on again over a fresh, mostly blank sheet to close the loop.

Keep the camera fixed. `Ar` is the only lettering; the Gemini connection ends with the star instead of a title. Check the `Ar` detail and the star's silhouette at actual 64×64 size during the later animation stage. Animation, further frames, and a GIF require separate approval after review of the first still.

## First-frame review

Review the actual 64×64 image and its nearest-neighbor enlarged copy together. The scene succeeds if a woman about to work on a blank sheet under a standing bulb is recognizable at native size, the orange cat reads in the upper frame, and the mood feels cute and cozy. The mug and paper should have distinct colors and silhouettes.

### Revision history

- `first.png`: generated with `gemini-nano-banana-2.1` from `prompt.txt`. The user liked the scene but requested the lamp on the right with a visible round bulb and filament. Its prepared frame and preview are retained for comparison.
- `first-v2.png`: edit of `first.png` from `prompt-v2.txt`. The user preferred the more visible bulb but found the composition left-heavy and the colors too blended. The lamp also looked suspended instead of standing on the desk.

### Fresh starting points

The user requested new images from scratch rather than another edit of `first-v2.png`. Each candidate uses only its own text prompt; `references/incandescent-bulb.png` records the supplied bulb reference for review but is not sent to the generator. All show a freestanding lamp on the right with visible glass and filament, a human drawing, and stronger color separation.

- `candidate-a`: clean 2D editorial illustration, balanced high three-quarter composition.
- `candidate-b`: deliberate lo-fi pixel art, high-angle desk view.
- `candidate-c`: simplified animation cel, diagonal composition and stronger outlines.

The user found A–C too restrained in color and composition. Candidate D adds a cute lo-fi character and a lived-in room, with no filament line inside the bulb. The earlier bulb photo remains a shape reference only; it was not an input to these generations.

- `candidate-d`: rounded 2D character illustration with a lavender hoodie and night window. The user liked this direction and requested a beautiful woman, completely blank notebook, coffee mug, and no drafting triangle.
- `candidate-d-v2`: edit of D following the initial request for a woman, blank notebook and coffee mug. The user then clarified that C was the desired base, so D-v2 is retained only as an exploration.
- `candidate-c-v2`: edit of C from `prompt-candidate-c-v2.txt` with `references/lofi-room.png` as a color and prop reference. The user selected a stronger supplied image afterward.
- `user-base.png`: user-supplied lo-fi pixel-art scene with the desired woman, sleeping cat, blank page, coffee and room. Its shaded articulated lamp is the only requested change.
- `user-base-lamp.png`: lamp-only edit of `user-base.png` from `prompt-user-base-lamp.txt`. The user accepted the visible filament line and requested a larger lamp in the foreground, a smaller coffee mug farther back, and less detail near the window.
- `user-base-lamp-v2.png`: composition edit of `user-base-lamp.png` from `prompt-user-base-lamp-v2.txt`. The lamp and coffee swap places and the window is simpler, but the user still finds too much detail at 64×64.
- `user-base-lamp-v3.png`: chunky-pixel simplification of v2 from `prompt-user-base-lamp-v3.txt`. The model kept too much fine detail. A temporary nearest-neighbor downsample looked harsh and was rejected by the user; it is not part of the review assets.
- `user-base-soft-v4.png`: softer redraw using v2 as a composition reference, from `prompt-user-base-soft-v4.txt`. The user did not approve it; the soft treatment lost the pixel-art character without buying readability.
- `user-grid-v5.png`: generated from the short, grid-directed `prompt-user-grid-v5.txt`, with `source/user-base-lamp-v2.png` attached as a layout and color reference only. `scripts/inspect_source.py` measured v2 at roughly 205 logical pixels of drawn detail, about 3.2x what a 64×64 frame holds, which is why every resize filter turned it to mud. The new prompt names six shapes, gives the bulb a quarter of the frame height, puts the dark window directly behind it, and asks for pixel blocks about one sixty-fourth of the canvas wide. Its frame `frames/frame_user-grid-v5.png` and preview `review/frame_user-grid-v5-8x.png` were prepared with the default `mode` pipeline and shown to the user. Review pending.

- `user-grid-v6.png`: recolor of `user-grid-v5.png` from `prompt-user-grid-v6.txt`. The user approved the new readability but found the colors flattened into a single amber-brown and supplied a lo-fi illustration as a color reference, saved as `references/lofi-girl-color.png` and attached to this generation for palette only. Sampled from it: pale teal `#BADDD8`, warm cream `#CCB69B`, terracotta `#C68A66`, muted olive `#967D5B`, burnt orange `#AC4E2A`, forest green `#2C3A2B`, brick red `#7D2622`. The sweater is now forest green, the chair brick red, the window desaturated teal-slate, and the bulb is the only saturated element. Prepared with `--saturation 1.0 --contrast 1.05` so the muted palette survives. Review pending.

- `user-grid-v7.png`: second recolor of `user-grid-v5.png`, from `prompt-user-grid-v7.txt`. The user rejected v6 as too daylit and confirmed the red sweater, orange cat and blue night of v5. This revision keeps that scheme but separates the three color families that had merged into one amber-brown tone: burgundy red sweater distinctly redder and darker than the medium reddish-brown desk, deep saturated midnight-blue window with cool slate silhouettes and small amber lit squares, bright orange cat against the blue, warm cream sheet, and a saturated amber bulb as the brightest shape. Review pending.

### Frame preparation

The first attempts exported with box averaging and 32 colors, which read as blurred, while a plain
nearest-neighbour test read as harsh noise. `scripts/prepare_frame.py` now flattens fine texture to
the locally dominant color, then gives each output pixel the color that covers most of its cell,
and quantizes to 64 colors without dithering. `--downsample box` still reproduces the old softer
export for comparison. The techniques behind this are recorded in
[docs/pixel-art-for-64x64.md](../../docs/pixel-art-for-64x64.md).

## References

- [Royal Society of Chemistry: argon and incandescent light bulbs](https://periodic-table.rsc.org/element/18/argon)
- [Google: Gemini 4 Argon and its blue announcement artwork](https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-4-argon/)
- [Google Gemini image-generation prompting guide](https://ai.google.dev/gemini-api/docs/image-generation#prompt-guide): specify style, medium, camera, composition, and the intended visual hierarchy.


## Animation prototype

Authorized after the user approved `user-grid-v7.png`. Built by `build_light_gif.py` into
`animation_frames/`, `review/prototype.gif` (64×64, 23 frames, 300 ms each, 6.9 s, 30 KB) and
`review/prototype-8x.gif`, with `review/prototype-contact-sheet.png` showing every frame at once.

### The loop

1. The room is dark; the lamp comes up over a blank sheet.
2. She draws an architect's note on the paper, stroke by stroke: ground line and height dimension
   first, then the elevation, its roof and bay divisions, the floor lines and ground hatch, a small
   plan view, and finally the dimension end ticks and a scale bar.
3. The room sinks into shadow while the lamp keeps burning.
4. The lamp steps forward and fills the frame, so what is inside the glass can be read: a pale blue
   `Ar` appears in the envelope, the argon that protects the filament.
5. The glass turns blue-violet and resolves into the four-point Gemini star, which fades as the warm
   lamp switches on again over a fresh sheet.

### What the model drew and what code drew

Two keyframes were generated for the drawing pose - `key-draw-mid.png` and `key-draw-done.png` from
their prompt files - then `key-draw-mid-v2.png` and `key-draw-done-v2.png` after the user asked for
a real engineering drawing instead of abstract shapes. All four failed the same way: the model
renders thin technical linework as scattered speckle once the image comes down to 64×64. They are
kept as a record of that limit.

Everything moving is therefore composited in code on the approved plate, which is also what keeps
the hair, cat, window and lamp from jittering between frames:

- the lamp turning on and the fade to shadow are blends toward night blue, with the bulb and its
  halo held at their own brightness;
- the architect's note is drawn with straight one-pixel strokes in two weights, pencil grey for the
  building and a lighter draft grey for the construction lines, dimensions and hatch. A first
  attempt at a box-and-arrow architecture diagram was rejected as abstract, and a second attempt
  drawn as a towered castle was rejected as childish; the present elevation with its height
  dimension, bay grid, hatched ground, plan view and scale bar reads as drafting;
- the argon reveal enlarges the bulb to fill the frame before naming the gas. Inside the
  13-pixel bulb of the still frame no lettering is legible, which is why the earlier small `Ar`
  could not be read. The large `Ar` is drawn by hand and is the only lettering in the loop;
- the Gemini star is a tapered polygon filled with a blue-to-violet gradient, growing out of the
  glass that just held the `Ar`.

### Prototype review

Watch the loop at both sizes. It succeeds if the lamp switching on reads as a reveal, the sheet
reads as an architect's working note while it is drawn, the `Ar` is unmistakable inside the glass,
and the star's four points stay sharp at native size. Known rough edge: the dimmed frames
desaturate the warm room toward grey-blue, which is a linear blend rather than a lighting pass.
Animation refinements and any final export still need separate approval.
