import numpy as np
import cv2
from motor import *
import time
def find_shape(c):
    peri = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, 0.04 * peri, True)
    return len(approx)

cam = cv2.VideoCapture('http://192.168.43.1:8080/video?x.mjpeg')
ret,source=cam.read()
i=0
while True:
    ret,source=cam.read()
    if(ret):
        cv2.putText(source,str(i),(100,100),cv2.FONT_HERSHEY_SIMPLEX,4,(255,255,255))
        cv2.imshow("source",source)
        cv2.waitKey(1)
        time.sleep(1)
        print i
        i=i+1
cv2.destroyAllWindows()
