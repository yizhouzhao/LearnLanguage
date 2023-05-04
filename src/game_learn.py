# main class for game translator
import string
import random

from pynput import keyboard
from paddleocr import PaddleOCR
from .translate import *
from .utils import *
 

class Learner():
    def __init__(self, 
            image_path = "./image/screenshot.png", 
            font_path = "./font/AaXingQiuHei-2.ttf",
            source_lang = "french",
            target_lang = "chinese",
            font_size = 40):
        
        Learner.source_lang = source_lang
        Learner.target_lang = target_lang
        self.image_path = image_path
        self.font_path = font_path
        self.source_lang = source_lang
        self.font_size = font_size

        self.ocr = PaddleOCR(use_angle_cls=True, lang=self.source_lang) # need to run only once to download and load model into memory
        if source_lang == "french":
            Learner.source_lang_code = "fr"
        elif source_lang == "japan":
            Learner.source_lang_code = "ja"
        else:
            Learner.source_lang_code = "en"    
        Learner.target_lang_code = "zh-CN" if target_lang == "chinese" else "en"

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
        translation = translate(text, Learner.target_lang_code, Learner.source_lang_code)
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
        scores = [line[1][1] for line in result]
        txts = [line[1][0] for line in result]
        if need_translation:
            txt_translations = self.perform_translation(txts)
        else:
            txt_translations = txts

        image_draw = draw_ocr_boxes(image, boxes, txt_translations, scores,
                                    font_path=self.font_path)
        # image_draw.show()
        if need_save:
            # generating random strings
            res = ''.join(random.choices(string.ascii_uppercase +
                                        string.digits, k=6))
            image_path = f"./image/{res}.png"
            image_draw.save(image_path)
            return image_draw, image_path

        else:
            return image_draw, None

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