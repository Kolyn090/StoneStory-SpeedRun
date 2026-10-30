
from pathlib import Path

import cv2
import numpy as np


# Configuration
MIN_BRIGHTNESS = 35
MIN_BORDER_COVERAGE = 0.70
MIN_PANEL_HEIGHT = 80
EDGE_MARGIN = 4


SCREENSHOT_DIR = Path(__file__).resolve().parent / "screenshot"


def find_description_bounds(image):
    """
    Detect long horizontal panel borders regardless of color.

    Accepts a BGR OpenCV image.
    Returns (top, bottom).
    """
    height, width = image.shape[:2]

    # Detect visible pixels regardless of hue.
    brightness = np.max(image, axis=2)
    visible = brightness >= MIN_BRIGHTNESS

    # Exclude the extreme horizontal edges.
    region = visible[:, EDGE_MARGIN:width - EDGE_MARGIN]

    # Fraction of each row containing visible pixels.
    coverage = np.mean(region, axis=1)

    # Long, solid lines have high row coverage.
    candidate_rows = np.where(
        coverage >= MIN_BORDER_COVERAGE
    )[0]

    if len(candidate_rows) < 2:
        raise ValueError("Not enough panel borders detected")

    # Group adjacent rows into single lines.
    groups = []
    current = [int(candidate_rows[0])]

    for y in candidate_rows[1:]:
        y = int(y)

        if y <= current[-1] + 2:
            current.append(y)
        else:
            groups.append(current)
            current = [y]

    groups.append(current)

    lines = [
        int(np.median(group))
        for group in groups
    ]

    # Select outermost horizontal borders.
    top = lines[0]
    bottom = lines[-1]

    if bottom - top < MIN_PANEL_HEIGHT:
        raise ValueError(
            "Detected borders are too close together"
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
