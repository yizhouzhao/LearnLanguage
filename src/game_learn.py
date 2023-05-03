# main class for game translator
from pynput import keyboard
from paddleocr import PaddleOCR
import mtranslate

from .utils import *
import string
import random
 

class Learner():
    def __init__(self, 
            image_path = "./image/screenshot.png", 
            font_path = "./font/AaXingQiuHei-2.ttf",
            source_lang = "french",
            target_lang = "chinese",
            font_size = 40):
        
        self.image_path = image_path
        self.font_path = font_path
        self.source_lang = source_lang
        self.font_size = font_size

        self.ocr = PaddleOCR(use_angle_cls=True, lang=self.source_lang) # need to run only once to download and load model into memory
        if source_lang == "french":
            self.source_lang_code = "fr"
        elif source_lang == "japan":
            self.source_lang_code = "ja"
        else:
            self.source_lang_code = "en"    
        self.target_lang_code = "zh-CN" if target_lang == "chinese" else "en"

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
        text = "\n".join(txts)
        translation = mtranslate.translate(text, self.target_lang_code, self.source_lang_code)
        print("....end translation....")
        translated_texts = translation.split("\n")
        return translated_texts

    def draw_ocr(self, result, need_translation = True, need_save = True):
        """
        Draw ocr
        """
        result = result[0]
        image = Image.open(self.image_path).convert('RGB')
        boxes = [line[0] for line in result]
        txts = [line[1][0] for line in result]
        if need_translation:
            txts = self.perform_translation(txts)

        scores = [line[1][1] for line in result]
        image_draw = draw_ocr_boxes(image, boxes, txts, scores,
                                    font_path=self.font_path)
        image_draw.show()
        if need_save:
            # generating random strings
            res = ''.join(random.choices(string.ascii_uppercase +
                                        string.digits, k=6))
            image_name = f"./image/{res}.png"
            image_draw.save(image_name)

        return image_draw

    ############################## keyboard event ##############################
    def on_press(self, key):   
        # Check if the key combination is pressed
        if key == keyboard.Key.print_screen:
            # Capture a screenshot
            self.get_screenshot()
            result = self.perform_ocr()
            image = self.draw_ocr(result)

        elif key == keyboard.Key.pause:
            exit()