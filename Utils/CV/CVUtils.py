import cv2
import numpy as np
class CVUtils():
    def __init__(self):
        pass

    def toGreyScale(img, method = cv2.COLOR_BGR2GRAY):
        return cv2.cvtColor(img, method)
    
    def denoise(img, kernelSize=5):
        return cv2.medianBlur(img,kernelSize)
 
    def threshold(image,min=0,max=255,method = [cv2.THRESH_BINARY, cv2.THRESH_OTSU]):
        return cv2.threshold(image, min, max, sum(method))[1]

    def dilate(image,kernel,ksize = (5,5), iterations = 1):
        kernel = np.ones(ksize,np.uint8)
        return cv2.dilate(image, kernel, iterations)

    def erode(image,ksize = (5,5), iterations = 1):
        kernel = np.ones(ksize,np.uint8)
        return cv2.erode(image, kernel, iterations)

    def opening(image,ksize = (5,5), method = cv2.MORPH_OPEN):
        kernel = np.ones(ksize,np.uint8)
        return cv2.morphologyEx(image, method, kernel)

    def canny(image,threshold1=100, threshold2=200, edges=None, apertureSize=None, L2gradient=None):
        # return cv2.Canny(image, threshold1, threshold2,edges,apertureSize,L2gradient)
        return cv2.Canny(image, threshold1, threshold2)

    def deskew(image):
        coords = np.column_stack(np.where(image > 0))
        angle = cv2.minAreaRect(coords)[-1]
        if angle < -45:
            angle = -(90 + angle)
        else:
            angle = -angle
        (h, w) = image.shape[:2]
        center = (w // 2, h // 2)
        M = cv2.getRotationMatrix2D(center, angle, 1.0)
        rotated = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
        return rotated

    def matchTemplate(image, template):
        return cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)

    def invert(image):
        return cv2.bitwise_not(image)