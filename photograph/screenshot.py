
from pathlib import Path

from helper.screen_getter import (
    get_window_with_title,
    get_chosen_region,
    get_unique_path,
)
from coordinates import matrix_boundary
from helper.window_name import window_name


def take_matrix_screenshot():
    """Capture the inventory matrix region of the game window."""

    window = get_window_with_title(window_name)

    if window is None:
        raise RuntimeError(f"Window not found: {window_name}")

    image = get_chosen_region(window, matrix_boundary)

    if image is None:
        raise RuntimeError("Failed to capture inventory matrix.")

    output_dir = Path(__file__).resolve().parent / "screenshot"
    output_dir.mkdir(parents=True, exist_ok=True)

    output_path = output_dir / "matrix.png"

    image.save(output_path)

    print(f"Screenshot saved to: {output_path}")

    return image


if __name__ == "__main__":
    take_matrix_screenshot()
