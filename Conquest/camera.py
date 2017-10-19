import numpy as np
import cv2
from motor import *

def find_shape(c):
    peri = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, 0.04 * peri, True)
    return len(approx)

cam = cv2.VideoCapture(1)
ret,source=cam.read()

while True:
    ret,source=cam.read()
    if(ret):
        cv2.imshow("source",source)
    else:
	print "no data"
    if(cv2.waitKey(10)==27):
        break
cv2.destroyAllWindows()
