import sys
import time
from pynput import mouse, keyboard

last_action_time = time.time()
currently_pressed_keys = set()


def print_delay_and_update():
    global last_action_time
    current_time = time.time()
    elapsed = current_time-last_action_time

    if elapsed > 0.05:
        print(f"    time.sleep({elapsed:.2f})")
    last_action_time = current_time


def onClick(x, y, button, pressed):
    if pressed:
        print_delay_and_update()
        btn_name = str(button).replace("Button.", "")
        print(f"    pyautogui.click({x}, {y}, button='{btn_name}')")
        sys.stdout.flush()


def onScroll(x, y, dx, dy):
    print_delay_and_update()
    print(f"    pyautogui.scroll({dy}, x={x}, y={y})")
    sys.stdout.flush()


def onPress(key):
    if key in currently_pressed_keys:
        return
    currently_pressed_keys.add(key)
    print_delay_and_update()
    try:
        print(f"    pyautogui.press('{key.char}')")
    except:
        key_name = str(key).replace("Key.", "")
        print(f"    pyautogui.press('{key_name}')")
    sys.stdout.flush()


def onRelease(key):
    global m_listener
    if key in currently_pressed_keys:
        currently_pressed_keys.remove(key)
    if key == keyboard.Key.esc:
        if m_listener:
            m_listener.stop()
        print("\n\n"+"="*28+" Logger Stopped "+"="*28+"\n")
        return False

# ------------------------- Program Starts Here ------------------------- #


print("\n"+"="*28+" Logger Started "+"="*28)
print("Press ESC to exit. Key spam is disabled\n\n")


with mouse.Listener(on_click=onClick, on_scroll=onScroll) as m_listener, keyboard.Listener(on_press=onPress, on_release=onRelease) as k_listener:
    m_listener.join()
    k_listener.join()
