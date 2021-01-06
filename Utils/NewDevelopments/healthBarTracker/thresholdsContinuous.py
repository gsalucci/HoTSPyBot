import cv2
import sys
import numpy as np
import mss
def nothing(x):
    pass



# Create a window
cv2.namedWindow('image', cv2.WINDOW_AUTOSIZE)
cv2.namedWindow('controls',cv2.WINDOW_AUTOSIZE)
# create trackbars for color change
cv2.createTrackbar('HMin','controls',0,179,nothing) # Hue is from 0-179 for Opencv
cv2.createTrackbar('SMin','controls',0,255,nothing)
cv2.createTrackbar('VMin','controls',0,255,nothing)
cv2.createTrackbar('HMax','controls',0,179,nothing)
cv2.createTrackbar('SMax','controls',0,255,nothing)
cv2.createTrackbar('VMax','controls',0,255,nothing)

# Set default value for MAX HSV trackbars.
cv2.setTrackbarPos('HMax', 'controls', 179)
cv2.setTrackbarPos('SMax', 'controls', 255)
cv2.setTrackbarPos('VMax', 'controls', 255)

# Initialize to check if HSV min/max value changes
hMin = sMin = vMin = hMax = sMax = vMax = 0
phMin = psMin = pvMin = phMax = psMax = pvMax = 0

with mss.mss() as sct:
    while(1):
        img = cv2.cvtColor(np.array(sct.grab({"top":0,"left":0,"width":1920,"height":1080})), cv2.COLOR_BGRA2BGR)
        # get current positions of all trackbars
        hMin = cv2.getTrackbarPos('HMin','controls')
        sMin = cv2.getTrackbarPos('SMin','controls')
        vMin = cv2.getTrackbarPos('VMin','controls')

        hMax = cv2.getTrackbarPos('HMax','controls')
        sMax = cv2.getTrackbarPos('SMax','controls')
        vMax = cv2.getTrackbarPos('VMax','controls')

        # Set minimum and max HSV values to display
        lower = np.array([hMin, sMin, vMin])
        upper = np.array([hMax, sMax, vMax])

        # Create HSV Image and threshold into a range.
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, lower, upper)
        output = cv2.bitwise_and(img,img, mask= mask)

        # Print if there is a change in HSV value
        if( (phMin != hMin) | (psMin != sMin) | (pvMin != vMin) | (phMax != hMax) | (psMax != sMax) | (pvMax != vMax) ):
            print("(hMin = %d , sMin = %d, vMin = %d), (hMax = %d , sMax = %d, vMax = %d)" % (hMin , sMin , vMin, hMax, sMax , vMax))
            phMin = hMin
            psMin = sMin
            pvMin = vMin
            phMax = hMax
            psMax = sMax
            pvMax = vMax

        # Display output image
        cv2.imshow('image',output)

        # Wait longer to prevent freeze for videos.
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cv2.destroyAllWindows()