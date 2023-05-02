from PIL import ImageGrab
from pynput import keyboard
from paddleocr import PaddleOCR, draw_ocr

# Define the key combination
COMBINATION = {keyboard.Key.print_screen} # (char='m')

# Define a variable to store the pressed keys
pressed_keys = set()

# Define a function to capture a screenshot
def capture_screenshot():
    # Capture the screen and save it to a file
    im = ImageGrab.grab()
    print("Captured screenshot")
    im.show()
    im.save('screenshot.png')

# Define a function to handle key press events
def on_press(key):
    # Add the pressed key to the set of pressed keys
    pressed_keys.add(key)
    
    # Check if the key combination is pressed
    if all(k in pressed_keys for k in COMBINATION):
        # Capture a screenshot
        capture_screenshot()

# Define a function to handle key release events
def on_release(key):
    # Remove the released key from the set of pressed keys
    pressed_keys.remove(key)

# Start listening for key events
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()