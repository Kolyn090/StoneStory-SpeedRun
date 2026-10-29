
from pynput import mouse, keyboard


def get_coords(x, y):
    print(f"Now at: ({x}, {y})")


def on_press(key):
    try:
        if key.char.lower() == 'q':
            print("Stopping coordinate tracker...")
            mouse_listener.stop()
            return False
    except AttributeError:
        pass


if __name__ == "__main__":
    mouse_listener = mouse.Listener(on_move=get_coords)
    keyboard_listener = keyboard.Listener(on_press=on_press)

    mouse_listener.start()
    keyboard_listener.start()

    print("Tracking mouse coordinates. Press Q to quit.")

    keyboard_listener.join()
    mouse_listener.stop()
    mouse_listener.join()
