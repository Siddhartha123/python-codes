import cv2
import numpy as np

def find_shape(c):

        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.04 * peri, True)
        if len(approx) == 3:
                shape = "Triangle"
        elif len(approx) == 4:
            shape = "4"
        else:
            shape = "Circle"
        return shape

def detect_color(px):
        if px[0]>240 and px[1]<10 and px[2]<10:
                return "blue"
        elif px[0]<10 and px[1]<10 and px[2]>240:
                return "red"
        elif px[0]<10 and px[1]>240 and px[2]<10:
                return "green"
        elif px[0]<10 and px[1]>240 and px[2]>240:
                return "yellow"

image=cv2.imread("4.png")
image_gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
image_bw=cv2.adaptiveThreshold(image_gray,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,51,0)
#cv2.imshow("adaptive",image_bw)
#image_bw=cv2.inRange(image_gray,30,230)
#cv2.imshow("thresh",image_bw)
cnts=cv2.findContours(image_bw.copy(),cv2.RETR_CCOMP,cv2.CHAIN_APPROX_SIMPLE)
cnts=cnts[0]
count=0
for j in range(0,len(cnts)):
    c1 = cnts[j]
    M1 = cv2.moments(c1)
    if M1['m00']!=0:
        cX1 = int((M1['m10'] / M1['m00']))
        cY1 = int((M1['m01'] / M1['m00']))
        area=M1['m00']
        shape = find_shape(cnts[j])
        if area>20:
            count=count+1
            cv2.drawContours(image, cnts,j, (206, 255, 39), 1)
            cv2.putText(image,str(shape), (cX1, cY1), cv2.FONT_ITALIC,0.5, (0,255,159), 1)
cv2.imshow("source",image)
print count
while True:
    if(cv2.waitKey(10)==27):
        break
cv2.destroyAllWindows()
