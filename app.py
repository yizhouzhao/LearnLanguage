from PIL import ImageGrab
from pynput import keyboard

from src.game_learn import GameLearn

# Define a function to capture a screenshot
def capture_screenshot():
    # Capture the screen and save it to a file
    im = ImageGrab.grab()
    print("Captured screenshot")
    im.show()
    im.save('screenshot.png')

# Define a function to handle key press events
def on_press(key):   
    # Check if the key combination is pressed
    if key == keyboard.Key.print_screen:
        # Capture a screenshot
        capture_screenshot()
    elif key == keyboard.Key.pause:
        exit()


if __name__ == "__main__":
    # game learn
    game_learn = GameLearn()
    # Start listening for key events
    with keyboard.Listener(on_press=game_learn.on_press) as listener:
        listener.join()