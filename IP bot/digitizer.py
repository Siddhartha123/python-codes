import cv2
import numpy as np
from trackBot import *
from final_code import *
from serial import Serial
import time
import math
import cv2
from math import pi,atan2,degrees
import time
cap=cv2.VideoCapture(1)
cap.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, 480)
count = 30
while count>0:
    _,image = cap.read()
    count-=1  
print 'crop out the start marker, white obstacle, yellow objects and end marker respectively'    
#points = part1(image)   
#print points 
count = 30
while count>0:
    _,image = cap.read()
    count-=1  
points=[((463, 38), 0), ((446, 425), 0), ((364, 425), 0), ((363, 423), 0), ((343, 329), 0), ((253, 315), 1), ((255, 218), 2), ((246, 149), 0), ((157, 127), 2), ((141, 30), 0), ((37, 15), 2), ((357, 27), 1), ((357, 27), 1), ((354, 228), 1), ((347, 304), 0), ((167, 329), 0), ((141, 431), 0), ((35, 444), 0)]
COM=raw_input("Enter COM Port to open\n")
robot=Serial("COM"+COM,baudrate=9600,timeout=1)
time.sleep(1)
for point in points:
    traverse(cap,point[0])
    if point[1]==2:
        sendByte('t')
    elif point[1]==1:
        sendByte('q')


def sendByte(b):
    global robot
    robot.write(b)
    while robot.inWaiting()==0:
        pass
    if robot.read()==b:
        print b
        return True
    else:
        return False

def find_shape(c):
    shape = "unidentified"
    peri = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, 0.049* peri, True)
    if len(approx) == 3 :
        shape = "Triangle"
    elif len(approx) ==4 :
        shape = "4-sided"
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
def orient(l2,l1):
    cX2=float(l2[0])
    cY2=float(l2[1])

    cX=float(l1[0])
    cY=float(l1[1])
    if not cX2==cX:

        angle=degrees(atan2((cY2-cY),(cX2-cX)))
    else:
        if cY2>=cY:
            angle=90
        else:
            angle=-90
    return angle

def rotate_left():
    sendByte('a')
def rotate_right():
    sendByte('d')
def stop():
    sendByte('s')
def forward():
    sendByte('w')