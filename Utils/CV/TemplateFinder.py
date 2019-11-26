import cv2
import mss
import numpy as np
class TemplateFinder():
    def __init__(self, **kwargs):
        #self.val2 = kwargs.get('val2',"default value")
        pass

    def find(self, zone, template, threshold, vis = False):
        methods = ['cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR', 'cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED']
        method = eval(methods[1])
        with mss.mss() as sct:
            img = np.array(sct.grab(zone))
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            w, h = template.shape[::-1]
            res = cv2.matchTemplate(img,template,method)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
            
            # if vis:
            #     # Visualisation of best match
            #     bottom_right = (max_loc[0] + w, max_loc[1] + h)
            #     cv2.rectangle(img,max_loc, bottom_right, 255, 2)
            #     plt.subplot(121),plt.imshow(res,cmap = 'gray')
            #     plt.title('Matching Result'), plt.xticks([]), plt.yticks([])
            #     plt.subplot(122),plt.imshow(img,cmap = 'gray')
            #     plt.title('Detected Point'), plt.xticks([]), plt.yticks([])
            #     plt.suptitle(max_val)
            #     plt.show()

            # If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
            if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
                top_left = min_loc
                if min_val < 1 - threshold:
                    return True
                else:
                    return False
            else:
                top_left = max_loc
                if max_val > threshold:
                    return True
                else:
                    return False