import cv2

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

source=cv2.imread("im.jpg")
gray=cv2.cvtColor(source,cv2.COLOR_BGR2GRAY)
thresh_mean=cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,5,0)
cnts=cv2.findContours(thresh_mean.copy(),cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
cnts=cnts[0]
for i in range (0,len(cnts)):
    c = cnts[i]
    M = cv2.moments(c)
    area=int(M['m00'])
    if area>100:
        cX = int((M['m10'] / M['m00']))
        cY = int((M['m01'] / M['m00']))
        cv2.drawContours(source, cnts,i, (0,255,159), 1)
        cv2.putText(source,str(find_shape(c)), (cX, cY), cv2.FONT_ITALIC,0.5, (0,255,159), 1)


cv2.imshow("MEAN",source)
cv2.imshow("thresh",thresh_mean)
cv2.waitKey(0)
