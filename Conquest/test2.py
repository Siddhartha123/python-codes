import numpy
import cv2

def find_shape(c):
    shape = "unidentified"
    peri = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, 0.02* peri, True)
    if len(approx) == 3:
        shape = "Triangle"
    elif len(approx) == 4:
        shape = "4-sided"
    else:
        shape = "Circle"
    #return len(approx)
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
    else:
        return 'obstacle'

cap=cv2.VideoCapture(1)
##cap is a 'VideoCapture()' object
while True:
    ret,img=cap.read()
    c_img=cv2.Canny(img,100,200)
    #cv2.imshow('image',img)
    #cv2.imshow('image',c_img)
    try:
    	#cnts,heirarchy=cv2.findContours(c_img,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        #cv2.drawContours(img,cnts,-1,(0,255,0),3)
        cnts_b = cv2.findContours(c_img.copy(),cv2.RETR_TREE ,cv2.CHAIN_APPROX_SIMPLE)
        cnts_b = cnts_b[0]
    except KeyError:
        print "error"
    l=[]
    for j in range(0,len(heirarchy_b[0])):
        if heirarchy_b[0][j][3]==-1:

            if heirarchy_b[0][j][2]!=-1:
                cv2.drawContours(img, cnts_b,-1, (206, 255, 39), 2)
                c1 = cnts_b[j]
                M1 = cv2.moments(c1)
                cX1 = int((M1['m10'] / M1['m00']))
                cY1 = int((M1['m01'] / M1['m00']))
                shape = find_shape(cnts_b[heirarchy_b[0][j][2]])
                c = cnts_b[heirarchy_b[0][j][2]]
                M = cv2.moments(c)
                cX = int((M["m10"] / M["m00"]))
                cY = int((M["m01"] / M["m00"]))
                #area=M["m00"]
                px=img[cY,cX]
                color=detect_color(px)
                l.append([shape,color,cY1,cX1])
                cv2.putText(img,shape, (cX, cY), cv2.FONT_ITALIC,0.5, (255, 255,255),2)

    cv2.imshow('image',img)
    if cv2.waitKey(20) & 0xFF == ord('q'):
        break

#s=type(frame)
cap.release()
#releases the object(important)
cv2.destroyAllWindows()
