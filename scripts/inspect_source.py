"""Report how much detail a generated pixel-art source carries, relative to a 64x64 frame."""

import argparse
from pathlib import Path

import numpy as np
from PIL import Image

TARGET = 64
MAX_PERIOD = 40


def grid_scores(image: Image.Image) -> list[tuple[int, float]]:
    """Score each candidate block size by how much of the edge energy lands on its grid lines."""
    pixels = np.asarray(image.convert("RGB"), dtype=np.int32)
    columns = np.abs(np.diff(pixels, axis=1)).sum(axis=(0, 2))
    rows = np.abs(np.diff(pixels, axis=0)).sum(axis=(1, 2))
    scores = []
    for period in range(2, MAX_PERIOD + 1):
        ratios = []
        for edges in (columns, rows):
            on_grid = np.arange(period - 1, len(edges), period)
            if len(on_grid) < 4:
                continue
            off_grid = np.delete(edges, on_grid)
            ratios.append(edges[on_grid].mean() / max(off_grid.mean(), 1e-9))
        if ratios:
            scores.append((period, float(np.mean(ratios))))
    scores.sort(key=lambda item: item[1], reverse=True)
    return scores


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("image", type=Path)
    args = parser.parse_args()

    with Image.open(args.image) as opened:
        image = opened.convert("RGB")
    side = min(image.width, image.height)
    colors = image.getcolors(maxcolors=1 << 24)
    scores = grid_scores(image)

    print(f"Canvas: {image.width}x{image.height}")
    print(f"Unique colors: {len(colors) if colors else 'more than 16M'}")
    print("Candidate pixel-block sizes, strongest first:")
    for period, score in scores[:5]:
        print(f"  {period:3d} px  score {score:.2f}  implies about {side / period:.0f} logical pixels")

    # Multiples of a true block size score almost as well, so prefer the smallest strong period
    # that the best-scoring one is a multiple of.
    best = scores[0][0]
    strong = [period for period, score in scores if score >= scores[0][1] * 0.90]
    divisors = [period for period in strong if best % period == 0]
    block = min(divisors or strong)
    logical = side / block
    print()
    if scores[0][1] < 1.15:
        print("Grid confidence is low: the edges are anti-aliased, so this is a painted pixel-art")
        print("facsimile rather than art drawn on a grid. Treat the size below as approximate.")
    print(f"Block size about {block} px, so roughly {logical:.0f} logical pixels of drawn detail.")
    print(f"A {TARGET}x{TARGET} frame holds {TARGET}.", end=" ")
    if logical > TARGET * 1.5:
        print(f"This source carries about {logical / TARGET:.1f}x too much:")
        print("fix it with fewer and larger shapes in the prompt, not with a different resize filter.")
    else:
        print("The detail budget is in range; readability now depends on value contrast.")


if __name__ == "__main__":
    main()
