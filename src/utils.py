from PIL import ImageGrab, Image, ImageFont, ImageDraw
import numpy as np
import math
import cv2
import re

def get_screen_size():
    """
    Get screen size
    """
    return ImageGrab.grab().size

# Define a function to capture a screenshot
def capture_screenshot(save_path = './image/screenshot.png', save_image = True):
    # Capture the screen and save it to a file
    im = ImageGrab.grab()
    print("Captured screenshot")
    # im.show()
    if save_image:
        im.save(save_path)

    return im

def draw_ocr_boxes(image,
             boxes,
             txts=None,
             scores=None,
             drop_score=0.5,
             font_path="./doc/fonts/simfang.ttf",
             font_scale=1.5):
    """
    Visualize the results of OCR detection and recognition
    args:
        image(Image|array): RGB image
        boxes(list): boxes with shape(N, 4, 2)
        txts(list): the texts
        scores(list): txxs corresponding scores
        drop_score(float): only scores greater than drop_threshold will be visualized
        font_path: the path of font which is used to draw text
    return(array):
        the visualized img
    """
    if scores is None:
        scores = [1] * len(boxes)
    
    draw_text = False if txts is None else True
    if draw_text:
        font = cv2.FONT_HERSHEY_SIMPLEX # font
        fontScale = font_scale # fontScale
        color = (255, 0, 0)  # Blue color in BGR
        thickness = 2 # Line thickness of 2 px
        
    
    box_num = len(boxes)
    for i in range(box_num):
        if scores is not None and (scores[i] < drop_score or
                                   math.isnan(scores[i])):
            continue
        box = np.reshape(np.array(boxes[i]), [-1, 1, 2]).astype(np.int64)
        image = cv2.polylines(np.array(image), [box], True, (255, 0, 0), 2)

    base = Image.fromarray(image).convert("RGBA")
    if draw_text:
        fnt = ImageFont.truetype(font_path, 40)
        # make a blank image for the text, initialized to transparent text color
        txt_image = Image.new("RGBA", base.size, (255, 255, 255, 0))
        # get a drawing context
        d = ImageDraw.Draw(txt_image)
        for i in range(box_num):
            if scores is not None and (scores[i] < drop_score or
                                   math.isnan(scores[i])):
                continue
            box = boxes[i]
            box_width = box[1][0] - box[0][0]
            box_height = box[2][1] - box[1][1]
            text = txts[i]

            org = (box[1][0] + 10, box[0][1] + box_height // 2 - 20)
            # print("org:", org, "text:", text)
            d.text(org, text, font=fnt, fill=(200, 10, 80, 255))

        # txt_image.show()
        base = Image.alpha_composite(base, txt_image)

    return base

def get_words_from_result(result):
    """
    Get words from results
    """
    txts = [line[1][0] for line in result[0]]
    print("txts", txts)
    line = " ".join(txts)
    line = re.sub(r"[^A-Za-z]", " ", line.strip())
    words = line.split()
    words = [word.lower() for word in words]
    return words


