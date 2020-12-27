import cv2
import mss
import numpy as np
import pytesseract as tesseract
from Utils.CV.CVUtils import CVUtils
class OCR():
    def __init__(self, **kwargs):
        config = r'--oem 3 --psm 6'

    def getText(image):
        config = r'--oem 3 --psm 6'
        found = ""
        image = CVUtils.toGreyScale(image)
        image = CVUtils.denoise(image)
        image = CVUtils.threshold(image)
        # image = CVUtils.opening(image)
        # image = CVUtils.canny(image)
        image = CVUtils.invert(image)
        found = tesseract.image_to_string(image,config=config)

        return found[:-1], image