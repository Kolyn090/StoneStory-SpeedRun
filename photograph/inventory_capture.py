
import time
from pathlib import Path
from pynput import keyboard

import pyautogui as pg

from coordinates import (
    matrix_boundary,
    DETAILS_OFFSET_Y,
    description_close_position,
)
from screenshot import take_description_screenshot
from mouse_dragger import scroll_next_page
from helper.screen_getter import get_window_with_title
from helper.window_name import window_name

STOP_REQUESTED = False

# ============================================================
# CONFIGURATION
# ============================================================

# Inventory grid
ROWS = 3
COLS = 4

# Number of rows we actually capture
ROWS_PER_PAGE = 2
ITEMS_PER_PAGE = ROWS_PER_PAGE * COLS  # 8

# Capture settings
PAGES_TO_CAPTURE = 1
START_PAGE = 1

# Number of items to capture per page.
# Set to None for all 12 items.
MAX_ITEMS_PER_PAGE = None

# Output directory
OUTPUT_DIR = Path(__file__).resolve().parent / "captures"

# Timing settings (seconds)
STARTUP_DELAY = 5.0

SELECT_DELAY = 0.25
DETAILS_HOVER_DELAY = 0.10
DETAILS_CLICK_DELAY = 0.30
CAPTURE_DELAY = 0.15
CLOSE_DELAY = 0.25

SCREENSHOT_MOUSE_DELAY = 0.15

MOUSE_MOVE_DURATION = 0.10
MOUSE_PRESS_DURATION = 0.05

PAGE_SCROLL_DELAY = 0.40

# Safety settings
OVERWRITE_EXISTING = False
DRY_RUN = False

# PyAutoGUI safety
pg.FAILSAFE = True
pg.PAUSE = 0.05

# Mouse position relative to the game window
SCREENSHOT_MOUSE_POSITION = description_close_position

# Pause after moving the cursor away
SCREENSHOT_MOUSE_DELAY = 0.3


def on_press(key):
    global STOP_REQUESTED

    try:
        if key.char and key.char.lower() == "q":
            STOP_REQUESTED = True
            print("\nStop requested. Finishing current item...")
    except AttributeError:
        pass


def move_mouse_away(window):
    """Move cursor away from the description before capture."""

    x = int(window.left + SCREENSHOT_MOUSE_POSITION[0])
    y = int(window.top + SCREENSHOT_MOUSE_POSITION[1])

    if DRY_RUN:
        print(f"[DRY RUN] Move mouse to ({x}, {y})")
        return

    pg.moveTo(x, y, duration=MOUSE_MOVE_DURATION)
    time.sleep(SCREENSHOT_MOUSE_DELAY)


# ============================================================
# COORDINATE HELPERS
# ============================================================

def get_cell_position(window, row, col):
    """Return absolute screen coordinates of a cell center."""

    left, top, right, bottom = matrix_boundary

    cell_width = (right - left) / COLS
    cell_height = (bottom - top) / ROWS

    x = left + (col + 0.5) * cell_width
    y = top + (row + 0.5) * cell_height

    return (
        int(window.left + x),
        int(window.top + y),
    )


# ============================================================
# MOUSE HELPERS
# ============================================================

def reliable_click(x, y):
    """Move to a position and perform a deliberate mouse click."""

    if DRY_RUN:
        print(f"[DRY RUN] Click ({x}, {y})")
        return

    pg.moveTo(
        x,
        y,
        duration=MOUSE_MOVE_DURATION,
    )

    pg.mouseDown(button="left")

    try:
        time.sleep(MOUSE_PRESS_DURATION)
    finally:
        pg.mouseUp(button="left")


def select_item(x, y):
    """Select an inventory item."""

    print(f"Selecting item at ({x}, {y})")

    reliable_click(x, y)

    if not DRY_RUN:
        time.sleep(SELECT_DELAY)


def click_details_button(cell_x, cell_y):
    """Click the Details button beneath the selected cell."""

    details_x = cell_x
    details_y = cell_y + DETAILS_OFFSET_Y

    print(f"Opening Details at ({details_x}, {details_y})")

    if DRY_RUN:
        print("[DRY RUN] Open Details")
        return

    pg.moveTo(
        details_x,
        details_y,
        duration=MOUSE_MOVE_DURATION,
    )

    time.sleep(DETAILS_HOVER_DELAY)

    pg.mouseDown(button="left")

    try:
        time.sleep(MOUSE_PRESS_DURATION)
    finally:
        pg.mouseUp(button="left")

    time.sleep(DETAILS_CLICK_DELAY)


def close_description(window):
    """Close the description panel using a configured position."""

    x = int(window.left + description_close_position[0])
    y = int(window.top + description_close_position[1])

    print(f"Closing description at ({x}, {y})")

    reliable_click(x, y)

    if not DRY_RUN:
        time.sleep(CLOSE_DELAY)


# ============================================================
# SCREENSHOT CAPTURE
# ============================================================

def capture_item_description(output_path):
    """Capture and save the current equipment description."""

    if DRY_RUN:
        print(f"[DRY RUN] Capture: {output_path}")
        return

    time.sleep(CAPTURE_DELAY)

    take_description_screenshot(output_path)

    print(f"Saved: {output_path}")


def capture_page(page_number, window):
    """Capture item descriptions on the current inventory page."""

    page_dir = OUTPUT_DIR / f"page_{page_number:03d}"

    if not DRY_RUN:
        page_dir.mkdir(parents=True, exist_ok=True)

    total_cells = ITEMS_PER_PAGE

    item_limit = (
        total_cells
        if MAX_ITEMS_PER_PAGE is None
        else min(MAX_ITEMS_PER_PAGE, total_cells)
    )

    for index in range(item_limit):
        if STOP_REQUESTED:
            break

        row = index // COLS
        col = index % COLS

        item_number = (
            (page_number - 1) * ITEMS_PER_PAGE
            + index + 1
        )

        x, y = get_cell_position(window, row, col)

        output_path = (
            page_dir / f"item_{item_number:04d}.png"
        )

        if output_path.exists() and not OVERWRITE_EXISTING:
            raise FileExistsError(
                f"Screenshot already exists: {output_path}"
            )

        print(
            f"\nItem {item_number} "
            f"(row {row + 1}, column {col + 1})"
        )

        # 1. Select item.
        select_item(x, y)

        # 2. Open Details beneath the cell.
        click_details_button(x, y)

        # 3. Move cursor away from the description.
        move_mouse_away(window)

        # 4. Capture description.
        try:
            capture_item_description(output_path)
        finally:
            close_description(window)


# ============================================================
# INVENTORY TRAVERSAL
# ============================================================

def capture_inventory():
    global STOP_REQUESTED

    STOP_REQUESTED = False

    print("Starting inventory capture...")
    print("Press Q to stop after the current item.")
    print("Move mouse to upper-left corner for emergency stop.")

    time.sleep(STARTUP_DELAY)

    page_number = START_PAGE

    with keyboard.Listener(on_press=on_press):
        while not STOP_REQUESTED:
            window = get_window_with_title(window_name)

            if window is None:
                raise RuntimeError("Game window not found")

            print(f"\nCapturing page {page_number}")

            capture_page(page_number, window)

            if STOP_REQUESTED:
                break

            scroll_next_page()
            time.sleep(PAGE_SCROLL_DELAY)

            page_number += 1

    print("\nCapture stopped.")


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":
    try:
        capture_inventory()

    except pg.FailSafeException:
        print("\nCapture aborted by PyAutoGUI failsafe.")

    except KeyboardInterrupt:
        print("\nCapture interrupted by user.")

    except Exception as exc:
        print(f"\nCapture stopped: {exc}")
        raise
