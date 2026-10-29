
from pathlib import Path

from helper.screen_getter import (
    get_window_with_title,
    get_chosen_region,
)
from coordinates import matrix_boundary, description_boundary
from helper.window_name import window_name


def take_screenshot(boundary, filename):
    """Capture a specified region of the game window."""

    window = get_window_with_title(window_name)

    if window is None:
        raise RuntimeError(f"Window not found: {window_name}")

    image = get_chosen_region(window, boundary)

    if image is None:
        raise RuntimeError(f"Failed to capture {filename}")

    output_dir = Path(__file__).resolve().parent / "screenshot"
    output_dir.mkdir(parents=True, exist_ok=True)

    output_path = output_dir / filename

    # Overwrite existing screenshot.
    image.save(output_path)

    print(f"Screenshot saved to: {output_path}")

    return image


def take_matrix_screenshot():
    """Capture the 4x3 inventory matrix."""
    return take_screenshot(matrix_boundary, "matrix.png")


def take_description_screenshot(output_path=None):
    window = get_window_with_title(window_name)

    if window is None:
        raise RuntimeError("Game window not found")

    image = get_chosen_region(window, description_boundary)

    if image is None:
        raise RuntimeError("Failed to capture description")

    if output_path is not None:
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        image.save(output_path)

    return image


if __name__ == "__main__":
    # take_matrix_screenshot()
    take_description_screenshot()
