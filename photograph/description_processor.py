
from pathlib import Path

import cv2
import numpy as np


SCREENSHOT_DIR = Path(__file__).resolve().parent / "screenshot"


def find_description_bounds(image):
    """
    Detect top and bottom horizontal gray borders.

    Returns (top, bottom), or raises ValueError.
    """
    height, width = image.shape[:2]

    # Identify gray border pixels.
    # Borders should be neutral-gray, not colorful.
    rgb = image.astype(np.int16)

    maximum = rgb.max(axis=2)
    minimum = rgb.min(axis=2)

    neutral = (maximum - minimum) <= 12
    brightness = (minimum >= 45) & (maximum <= 190)

    border_mask = neutral & brightness

    candidates = []

    min_line_length = int(width * 0.45)

    for y in range(height):
        row = border_mask[y]

        # Find longest contiguous horizontal run.
        padded = np.pad(
            row.astype(np.int8),
            (1, 1),
            constant_values=0
        )

        changes = np.diff(padded)
        starts = np.where(changes == 1)[0]
        ends = np.where(changes == -1)[0]

        if len(starts) == 0:
            continue

        longest = int(np.max(ends - starts))

        if longest >= min_line_length:
            candidates.append(y)

    if len(candidates) < 2:
        raise ValueError(
            "Could not detect two description borders."
        )

    # Combine nearby detected rows into line groups.
    groups = [[candidates[0]]]

    for y in candidates[1:]:
        if y - groups[-1][-1] <= 3:
            groups[-1].append(y)
        else:
            groups.append([y])

    lines = [
        int(np.median(group))
        for group in groups
    ]

    if len(lines) < 2:
        raise ValueError(
            "Only one horizontal border detected."
        )

    top = lines[0]
    bottom = lines[-1]

    if bottom - top < 80:
        raise ValueError(
            "Detected panel height is too small."
        )

    return top, bottom


def crop_description(
    input_path=None,
    output_path=None,
    padding=3,
):
    if input_path is None:
        input_path = SCREENSHOT_DIR / "description.png"

    if output_path is None:
        output_path = (
            SCREENSHOT_DIR / "description_cropped.png"
        )

    image = cv2.imread(str(input_path))

    if image is None:
        raise FileNotFoundError(input_path)

    top, bottom = find_description_bounds(image)

    height = image.shape[0]

    crop_top = max(0, top + 20)
    crop_bottom = min(height, bottom - 20)

    cropped = image[crop_top:crop_bottom, :]

    output_path = Path(output_path)
    output_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    if not cv2.imwrite(str(output_path), cropped):
        raise OSError(f"Cannot save {output_path}")

    print(f"Top border: {top}")
    print(f"Bottom border: {bottom}")
    print(f"Panel height: {bottom - top}")
    print(f"Saved: {output_path}")

    return cropped


if __name__ == "__main__":
    crop_description()
