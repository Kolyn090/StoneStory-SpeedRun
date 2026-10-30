from screen_getter import get_window_with_title
from window_name import window_name


# Rescale the window to fit the requirement
if __name__ == '__main__':
    chosen_window = get_window_with_title(window_name)
    top, bottom, left, right = 0, 650, 0, 800

    # Calculate the width and height based on the bounds
    width = right - left
    height = bottom - top

    if chosen_window:
        chosen_window.activate()

        chosen_window.moveTo(left, top)
        chosen_window.resizeTo(width, height)
        print(f"Window resized to top-left ({left}, {top}) with width {width} and height {height}.")
    else:
        print('Window not found, cannot rescale')
