
import time
import pyautogui as pg

from helper.screen_getter import get_window_with_title
from helper.window_name import window_name


SCROLL_POSITION = (765, 216)
SCROLL_STEPS_PER_PAGE = 6
SCROLL_DELAY = 0.1


def scroll_next_page():
    """Advance the inventory by one 4x3 page."""

    window = get_window_with_title(window_name)

    if window is None:
        raise RuntimeError("Game window not found")

    window.activate()
    time.sleep(0.3)

    x = window.left + SCROLL_POSITION[0]
    y = window.top + SCROLL_POSITION[1]

    pg.moveTo(x, y)

    for _ in range(SCROLL_STEPS_PER_PAGE):
        pg.scroll(-1)
        time.sleep(SCROLL_DELAY)

    time.sleep(0.5)


if __name__ == "__main__":
    scroll_next_page()
