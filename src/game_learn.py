# main class for game translator
from pynput import keyboard
from paddleocr import PaddleOCR
from translate import Translator

from .utils import *

class GameLearn():
    def __init__(self, 
            image_path = "./image/screenshot.png", 
            font_path = "./font/SourceCodePro-Black.ttf",
            source_lang = "french",
            target_lang = "chinese",
            font_size = 40):
        
        self.image_path = image_path
        self.font_path = font_path
        self.source_lang = source_lang
        self.font_size = font_size

        self.ocr = PaddleOCR(use_angle_cls=False, lang=self.source_lang) # need to run only once to download and load model into memory
        self.translator = Translator(from_lang='fr', to_lang='zh')
        
        print("init complete:", self.image_path)


    def get_screenshot(self):
        """
        Get screenshot
        """
        capture_screenshot(self.image_path)

    def perform_ocr(self):
        print("....performing ocr inference....")
        ocr_result = self.ocr.ocr(self.image_path, cls=True)
        return ocr_result

    def perform_translation(self, txts):
        print("....performing translation....")
        translation_texts = []
        for text in txts:
            translation_text = self.translator.translate(text)
            translation_texts.append(translation_text)
        print("....end translation....")
        
        return translation_texts

    def draw_ocr(self, result, need_translate = True):
        """
        Draw ocr
        """
        result = result[0]
        image = Image.open(self.image_path).convert('RGB')
        boxes = [line[0] for line in result]
        txts = [line[1][0] for line in result]
        if need_translate:
            txts = self.perform_translation(txts)

        scores = [line[1][1] for line in result]
        image_draw = draw_ocr_boxes(image, boxes, txts, scores)
        image_draw.show()

    ############################## keyboard event ##############################
    def on_press(self, key):   
        # Check if the key combination is pressed
        if key == keyboard.Key.print_screen:
            # Capture a screenshot
            self.get_screenshot()
            result = self.perform_ocr()
            self.draw_ocr(result)

        elif key == keyboard.Key.pause:
            exit()