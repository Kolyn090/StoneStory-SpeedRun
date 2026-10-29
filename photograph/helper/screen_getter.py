import cv2
import platform
if platform.platform().startswith('Win'):
    import pygetwindow as gw
import numpy as np
from PIL import Image, ImageGrab
from pathlib import Path

# This function will look for a window with a specific title
def get_window_with_title(title):
    def get_window_list_win():
        return gw.getAllWindows()

    def get_win_window():
        for window in get_window_list_win():
            if window.title.startswith(title):
                return window
        return None

    if platform.platform().startswith('Win'):
        return get_win_window()
    else:
        return None


def get_screenshot_of_chosen_window(window) -> Image.Image:
    def run_win():
        x = window.left
        y = window.top
        h = window.height
        w = window.width
        return ImageGrab.grab(
            bbox=(x, y, x + w, y + h)
        )

    if platform.system() == 'Windows':  # Better way to check OS
        return run_win()
    return None


def get_chosen_region(window, region) -> Image.Image:
    def run_win():
        x = window.left + region[0]
        y = window.top + region[1]
        w = region[2] - region[0]
        h = region[3] - region[1]

        return ImageGrab.grab(bbox=(x, y, x + w, y + h))

    if platform.system() == 'Windows':  # Better way to check OS
        return run_win()
    return None


def get_chosen_region_cv2(window, region) -> np.ndarray:
    def run_win():
        img = get_chosen_region(window, region)
        img_cv = np.array(img)

        return cv2.cvtColor(img_cv, cv2.COLOR_RGB2BGR)

    if platform.system() == 'Windows':
        return run_win()
    return None



def get_unique_path(filename):
    path = Path(filename)

    # Create the destination folder if necessary.
    path.parent.mkdir(parents=True, exist_ok=True)

    if not path.exists():
        return path

    stem = path.stem
    suffix = path.suffix
    parent = path.parent

    i = 1
    while True:
        new_path = parent / f"{stem}_{i}{suffix}"
        if not new_path.exists():
            return new_path
        i += 1


if __name__ == '__main__':
    chosen_window = get_window_with_title('Stone Story')
    screen = get_screenshot_of_chosen_window(chosen_window)
    add_x = 155
    crop_bound = (117+add_x, 198, 770+add_x, 621)
    game_zone = screen.crop(crop_bound)
    game_zone.save(get_unique_path('test.png'))
