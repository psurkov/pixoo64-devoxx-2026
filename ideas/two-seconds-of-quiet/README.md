# Two Seconds of Quiet

**Status:** the first frame is approved and the 30-frame loop is built and awaiting review.

## Core scene

The same desk at night as [The Light on the Page](../the-light-on-the-page/README.md), with the
lamp taken out and nothing to reveal. A young woman sits writing. A mug of coffee steams beside
her, an orange cat sleeps along the window ledge, and the blue city sits quietly behind them.

There is no Gemini, no argon, no star and no lettering anywhere in this piece. It is a two-second
loop whose whole job is to feel calm and to move smoothly. Where the other two ideas carry a
message, this one carries only mood: a lo-fi night, a warm room and small continuous motion.

## Proposed first static 64×64 frame

- The approved composition of `the-light-on-the-page/source/user-grid-v7.png`, minus the lamp. The
  woman sits at the left in her burgundy sweater, her pencil on a cream sheet.
- The coffee mug moves from behind the lamp into the lamp's old place in the lower right, large
  enough to be one of the first shapes noticed, with room above it for steam.
- The orange cat keeps the top edge. The deep blue night window keeps its building silhouettes and
  amber lit squares.
- Without the bulb, the warm light now comes from off-frame, so the room keeps its amber pool over
  the paper and the mug casts the brightest highlight.

## The motion, and why it fits 30 frames

Thirty frames is the contest ceiling, so at about 15 frames per second the loop is two seconds
long and every frame is a real step rather than a held pose. That is enough for several slow cycles
running at once, each one a few pixels of travel:

- **Steam from the mug.** Three or four pixels drifting up and fading, on a cycle that divides into
  thirty so it returns to its start.
- **The cat breathing.** Its back rises and falls by one pixel over the full loop, with one ear
  twitch somewhere in the middle.
- **Her writing hand.** A small repeated gesture of the hand and pencil rather than text that
  accumulates: a two-second loop cannot add words and still return to its first frame without a
  visible jump. What she has written stays as it is.
- **The city.** One or two lit windows fade up and down, slightly out of step with each other.
- **A leaf or the curtain edge.** A single pixel of sway, slowest of all.

Nothing in the frame travels more than three or four pixels. At 64×64 that is the difference
between a scene that breathes and a scene that twitches.

### Loop and timing notes

The loop has to close seamlessly, so every cycle length must divide thirty: cycles of 30, 15, 10 or
6 frames. One cycle that does not divide evenly will show as a stutter at the loop point.

GIF frame delays are stored in hundredths of a second, so exactly 15 fps is not expressible. The
nearest options are 70 ms per frame, giving 14.3 fps and a 2.10 s loop, or 60 ms, giving 16.7 fps
and a 1.80 s loop. 70 ms is the closer match to the requested feel. Jixoo's recipes also warn that
Pixoo hardware may stop looping past about 30 to 32 frames, so thirty frames is both the budget and
the limit.

## Color direction

The palette of `user-grid-v7.png`: burgundy sweater, reddish-brown desk, warm cream paper, bright
orange cat, deep midnight-blue window with amber lit squares. The lamp's saturated amber is gone,
so the warmest point in the frame becomes the coffee and the pool of light on the paper.

## What a generation is needed for

One new source: the approved scene redrawn without the lamp and with the mug moved forward. The
motion itself is better done in code from that single plate, the way
`the-light-on-the-page/build_light_gif.py` works, because small sprite nudges and fades stay crisp
while the model cannot hold fine detail steady between generations. No animation keyframes from the
model should be needed at all.

## Review target

The still succeeds if the room reads as cozy and lo-fi at native size without the lamp carrying it,
and the mug reads clearly in the lower right. The loop succeeds if it feels continuous: no element
snapping back at the loop point, no motion fast enough to read as a glitch, and the whole thing
calm enough to watch repeatedly.


## First-frame revision history

- `first-v2.png`: edit of `first.png` from `prompt-v2.txt`. The user asked for her to be reading
  rather than writing, and for the drink to be unmistakably coffee. The loose sheet became an open
  book with two pages and a centre line, the pencil is gone and her hand rests on the page; the mug
  became a straight-sided ceramic mug with a thick handle and dark coffee. Reading also removes the
  loop problem that writing had: there is no accumulating text to reset at the loop point.
- `frame_001_v3.png`: `first-v2.png` with coffee steam added by `build_loop.py`. The user asked for
  a small plume. It is drawn in code because it is the motion of this piece and amounts to a handful
  of single pixels per frame. Measuring the frame first was necessary: the ceramic rim sits at rows
  37-38 with the coffee at rows 39-41, and the bright page fills the space straight above the mug,
  so a pale wisp rising vertically was invisible. The plume now leans right into the clear wood at
  x 54..60, six puffs on one shared cycle, each fading as it climbs. `review/frame_001_v3-8x.png`
  is the preview and `review/frame_001_v3-steam-phases.png` shows six phases of the cycle side by
  side. Review pending.
- `first.png`: edit of `source/approved-room.png` from `prompt.txt`, generated with
  `gemini-nano-banana-2.1`. `approved-room.png` is a copy of the approved
  `the-light-on-the-page/source/user-grid-v7.png`, kept here so this idea's folder holds its own
  inputs. The prompt removed the bulb, its base and its halo, and moved the coffee mug into the
  space the lamp left, drawn larger with clear empty space above it for the steam that the
  animation will add in code. Frame `frames/frame_001.png` and preview `review/frame_001-8x.png`
  were prepared with the default `mode` pipeline and shown to the user. Review pending.


## Animation loop

Authorized after the user approved `frame_001_v3.png`. Built by `build_loop.build_loop()` into
`animation_frames/`, `review/prototype.gif` (64×64, 30 frames, 70 ms each, 2.10 s) and
`review/prototype-8x.gif`, with `review/prototype-contact-sheet.png` showing every frame.

Thirty frames at 70 ms is 14.3 frames per second, the closest a GIF can come to the requested 15:
delays are stored in hundredths of a second, so 70 ms gives a 2.10 s loop and 60 ms would give
1.80 s. Thirty frames is also the contest ceiling and the point where Pixoo hardware may stop
looping.

The pages carry text, also drawn in code: the user found the open book too empty. The first attempt
ruled every row horizontally, which read as lined notebook paper and, worse, sat at an angle to the
pages themselves. The pages are a wedge in perspective, with their top and bottom edges running at
different angles, so each line is now placed at a constant fraction of the way down the page rather
than along a constant row: `page_edges` reads the top and bottom row of open page for every column,
and a line interpolates between them. Lines lean with the page as a result. They are split at the
spine into two columns, their lengths vary from a fixed pattern, and the ink is a light grey-brown,
because at one pixel a darker line reads as a rule and not as writing. The plate with text is saved
as `frames/frame_001_v4.png` with its preview in `review/frame_001_v4-8x.png`.

Everything moves in code, from the single approved plate. Nothing travels more than one pixel,
because at 64×64 anything larger stops reading as breathing and starts reading as a jump:

- **Coffee steam**, six puffs on one 30-frame cycle, leaning right into the clear wood and fading
  as they climb.
- **The cat breathing**, its body raised by one pixel while the cycle's sine is above 0.5, with the
  row it leaves behind refilled so no gap opens. One ear twitches on frames 13 and 14.
- **The city**, three groups of lit windows dimming and brightening on cycles of 15, 10 and 30
  frames, so they drift out of step with each other.

Every cycle length divides thirty, so each one returns to its own start and the seam is invisible.

### Loop review

Watch it at both sizes. It succeeds if the room feels continuous and calm, the steam reads as steam
rather than as flickering pixels, the cat reads as breathing, and nothing snaps at the loop point.
Known rough edge: the cat's lift moves a tight rectangle, so a pixel of the window ledge behind it
travels with the cat; a per-pixel cat mask would fix it if the motion reads wrong. A final export
still needs separate approval.
