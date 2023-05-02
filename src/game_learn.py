# main class for game translator
from pynput import keyboard
from paddleocr import PaddleOCR

from .utils import *

class GameLearn():
    def __init__(self, 
            image_path = "./image/screenshot.png", 
            font_path = "./font/SourceCodePro-Black.ttf",
            lang = "french",
            font_size = 40):
        
        self.image_path = image_path
        self.font_path = font_path
        self.lang = lang
        self.font_size = font_size

        self.ocr = PaddleOCR(use_angle_cls=True, use_tensorrt = False, lang=self.lang) # need to run only once to download and load model into memory
        self.ocr_result = None
        print("init complete:", self.image_path)

    # keyboard event
    def on_press(self, key):   
        # Check if the key combination is pressed
        if key == keyboard.Key.print_screen:
            # Capture a screenshot
            self.get_screenshot()
        elif key == keyboard.Key.pause:
            exit()


    def get_screenshot(self):
        """
        Get screenshot
        """
        capture_screenshot(self.image_path)

    def perform_ocr(self):
        self.ocr_result = self.ocr.ocr(self.image_path, cls=True)

    def perform_translation(self):
        pass

    def draw_text(self):
        pass