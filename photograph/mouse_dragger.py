
import time
import pyautogui as pg

from helper.screen_getter import get_window_with_title
from helper.window_name import window_name


def scroll_inventory_down(steps=5, delay=0.1):
    window = get_window_with_title(window_name)

    if window is None:
        raise RuntimeError("Game window not found")

    window.activate()
    time.sleep(0.3)

    # Position mouse inside inventory grid
    x = window.left + 765
    y = window.top + 216

    pg.moveTo(x, y)

    # Send individual scroll events
    for _ in range(steps):
        pg.scroll(-1)
        time.sleep(delay)

    time.sleep(0.5)


if __name__ == "__main__":
    scroll_inventory_down(steps=9, delay=0.1)
