# Making a generated image read at native 64x64

Notes distilled from [SpriteCook: Nano Banana pixel art for games](https://www.spritecook.ai/blog/nanobanana-pixel-art-for-games)
and from measurements of this repository's own generations.

## What the model actually does

The model paints the *appearance* of pixel art on a large canvas. It does not draw on a 64x64 grid.
Measured on our own sources (`scripts/inspect_source.py`):

| source | canvas | apparent pixel block | effective logical size | unique colors |
| --- | --- | --- | --- | --- |
| `user-base.png` | 1366 | ~20 px | ~68 | 217k |
| `user-base-lamp-v2.png` | 1024 | ~5 px | ~205 | 216k |
| `user-base-soft-v4.png` | 1024 | ~25 px | ~41 | 116k |
| `user-grid-v5.png` (after these rules) | 1024 | ~16 px | ~64 | 68k |

Two consequences:

- A source whose block size implies 200 logical pixels carries roughly 3x more detail than a
  64x64 frame can hold. Shrinking it averages three logical pixels into one and the result turns
  to mud. This is a *composition* failure, not a resampling failure.
- Hundreds of thousands of colors mean the edges are anti-aliased. Real pixel art has hard edges,
  so the grid has to be recovered after generation rather than assumed.

## Prompting rules that follow from this

1. **State the subject, the camera and the purpose in a few direct sentences.** "A 2D game scene"
   is a stronger instruction than a paragraph of style adjectives. Long prompts make the model add
   detail; detail is the enemy here.
2. **Name the target grid and the block size together.** Asking for "64x64" alone is ignored.
   Asking for art *designed on a 64x64 grid and shown with large square pixel blocks* produces
   bigger blocks, which is what survives the downsample.
3. **Budget the objects.** A 64x64 frame holds about five to seven shapes that a viewer can name.
   List exactly those and say the rest of the frame is quiet. Give each named shape a minimum size
   in output pixels ("the bulb fills about a quarter of the frame height").
4. **Separate the shapes by value, not by outline.** Outlines are one logical pixel wide and are
   the first thing lost. Neighbouring masses must differ in lightness.
5. **Put the light source against dark.** A glowing object drawn over pale paper and light wood has
   no silhouette left after downsampling.
6. **Do not constrain the palette.** Colour count is not what breaks readability here; shape size
   and value contrast are. (User preference for this project, and it matches the measurements.)
7. **Verify, then fix the grid.** Always inspect the actual 64x64 output, never only the large
   source. Expect to repair the grid in code afterwards.

## Repairing the grid in code

`scripts/prepare_frame.py` implements the repair. Averaging (`BOX`) blurs flat color masses
together; point sampling (`NEAREST`) picks one arbitrary pixel per cell and turns anti-aliased
edges into noise. Neither is right for a painted pixel-art facsimile.

The default `mode` pipeline instead:

1. optional square crop, aligned to the detected block grid;
2. pre-quantize the source to a working palette, which collapses anti-aliasing back into flat masses;
3. for each of the 64x64 output cells, take the **dominant** color of that cell, so an output pixel
   is the color that actually covers most of the area - crisp like `NEAREST`, stable like `BOX`;
4. light contrast and saturation lift, then a final quantization without dithering.

Use `scripts/inspect_source.py <image>` to read a source's block size before preparing a frame, and
`--downsample box` only to reproduce the older, softer look for comparison.
