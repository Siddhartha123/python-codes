import numpy as np
import cv2
..

def find_shape(c):
    peri = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, 0.04 * peri, True)
    return len(approx)

camL = cv2.VideoCapture(1)
ret,sourceL=camL.read()

camR = cv2.VideoCapture(2)
ret,sourceR=camR.read()
fourccL=cv2.cv.CV_FOURCC(*'DIVX')
fourccR=cv2.cv.CV_FOURCC(*'DIVX')
outL=cv2.VideoWriter('outputL.avi',fourccL,20.0,(1280,720))
outR=cv2.VideoWriter('outputR.avi',fourccR,20.0,(1280,720))
while True:
    ret,sourceL=camL.read()
    ret,sourceR=camR.read()
    outL.write(sourceL)
    outR.write(sourceR)
    if(ret):
        cv2.imshow("LEFT",sourceL)
        cv2.imshow("RIGHT",sourceR)
    else:
	print "no data"
    if(cv2.waitKey(10)==27):
        break
outL.release()
outR.release()
cv2.destroyAllWindows()
