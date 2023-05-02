from PIL import ImageGrab, Image
import numpy as np
import math
import cv2

# Define a function to capture a screenshot
def capture_screenshot(save_path = './image/screenshot.png'):
    # Capture the screen and save it to a file
    im = ImageGrab.grab()
    print("Captured screenshot")
    im.show()
    im.save(save_path)

def draw_ocr_boxes(image,
             boxes,
             txts=None,
             scores=None,
             drop_score=0.5,
             font_path="./doc/fonts/simfang.ttf",
             font_scale=1):
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
        thickness = 5 # Line thickness of 2 px
        
    
    box_num = len(boxes)
    for i in range(box_num):
        if scores is not None and (scores[i] < drop_score or
                                   math.isnan(scores[i])):
            continue
        box = np.reshape(np.array(boxes[i]), [-1, 1, 2]).astype(np.int64)
        image = cv2.polylines(np.array(image), [box], True, (255, 0, 0), 2)
        if draw_text:
            text = txts[i]
            # Using cv2.putText() method
            org = (box[1][0][0] + 10, box[0][0][1] + 10)
            image = cv2.putText(image, text, org, font, 
                            fontScale, color, thickness, cv2.LINE_AA)

    return image


