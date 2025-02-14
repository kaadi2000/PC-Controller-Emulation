import pygame
import time
from pynput.keyboard import Controller, Key

pygame.init()
pygame.joystick.init()

keyboard = Controller()

isControllerConnected = False

def checkController():
    if pygame.joystick.get_count() == 0:
        print("No Controller detected. Connect controller!!")
        isControllerConnected = False
        time.sleep(5.0)
        return False
    isControllerConnected = True
    connectController()
    return True
    

def connectController():
    global joystick
    joystick = pygame.joystick.Joystick(0)
    joystick.init()

button_map = {
    3: [Key.ctrl, 'h'],  # Y Button → CTRL + H (Together)
    0: [Key.enter],  # A Button → ENTER
    1: [Key.ctrl, Key.backspace],  # B Button → CTRL + BACKSPACE
}

direction_map = {
    "left_right": (0, Key.left, Key.right),  # Left Stick X-Axis
    "up_down": (1, Key.up, Key.down),  # Left Stick Y-Axis
}

lastPressed = {}

DEBOUNCE_DELAY = 0.15  # 150ms per movement step

def press_combo(keys):
    """ Presses and releases multiple keys together. """
    for key in keys:
        keyboard.press(key)
    time.sleep(0.05)  # Small tap delay
    for key in reversed(keys):  # Reverse order to release properly
        keyboard.release(key)

def run():
    try:
        while True:
            while checkController() == False:
                checkController()
            pygame.event.pump()

            # Handle button presses (Y, A, B only)
            for button, key_combo in button_map.items():
                if joystick.get_button(button):  # If button is pressed
                    currentTime = time.time()
                    if button not in lastPressed or (currentTime - lastPressed[button] > DEBOUNCE_DELAY):
                        press_combo(key_combo)  # Press both keys together
                        lastPressed[button] = currentTime
                    
            dpad_x, dpad_y = joystick.get_hat(0)
            currentTime = time.time()

            if dpad_x == -1 and (Key.left not in lastPressed or currentTime - lastPressed[Key.left] > DEBOUNCE_DELAY):
                press_combo([Key.left])
                lastPressed[Key.left] = currentTime

            if dpad_x == 1 and (Key.right not in lastPressed or currentTime - lastPressed[Key.right] > DEBOUNCE_DELAY):
                press_combo([Key.right])
                lastPressed[Key.right] = currentTime

            if dpad_y == 1 and (Key.up not in lastPressed or currentTime - lastPressed[Key.up] > DEBOUNCE_DELAY):
                press_combo([Key.up])
                lastPressed[Key.up] = currentTime

            if dpad_y == -1 and (Key.down not in lastPressed or currentTime - lastPressed[Key.down] > DEBOUNCE_DELAY):
                press_combo([Key.down])
                lastPressed[Key.down] = currentTime

            for _, (axis, neg_key, pos_key) in direction_map.items():
                value = joystick.get_axis(axis)

                if value < -0.5 and (neg_key not in lastPressed or currentTime - lastPressed[neg_key] > DEBOUNCE_DELAY):
                    press_combo([neg_key])
                    lastPressed[neg_key] = currentTime

                elif value > 0.5 and (pos_key not in lastPressed or currentTime - lastPressed[pos_key] > DEBOUNCE_DELAY):
                    press_combo([pos_key])
                    lastPressed[pos_key] = currentTime

            time.sleep(0.01)

    except KeyboardInterrupt:
      print("Exiting gracefully...")

    finally:
        pygame.quit()

run()