import cv2
import numpy as np


def get_key_points(path):
    img = cv2.imread(path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    corners = cv2.goodFeaturesToTrack(gray, 25, 0.01, 10)
    if corners is None:
        return []
    corners = np.int0(corners)
    kp = []
    for i in corners:
            kp.append(i.ravel())
    return kp
