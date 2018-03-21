import numpy as np
import cv2
from function import *
from bot_detection import *

'''
*Function Name- rotate
*Input :- a string
*Output :- a list consisting of bot's x co-ord ,y co-ord and the angle made by the bot w.r.t. the x-axis
*Logic:- as the markers placed on the bot are unique, hence by masking the actual frame with the color-range of the markers(in HSV colorspace), the actual co-ord of the markers and hence the bot is determined
Example trackBot(frame,x,y)
'''



'''
*Function Name- trackBot
*Input :- feed from the camera, point where the bot needs to go
*Output :- a list consisting of bot's x co-ord ,y co-ord and the angle made by the bot w.r.t. the x-axis
*Logic:- as the markers placed on the bot are unique, hence by masking the actual frame with the color-range of the markers(in HSV colorspace), the actual co-ord of the markers and hence the bot is determined
Example trackBot(frame,x,y)
'''

def trackBot(frame,x,y,list_of_max_vals,list_of_min_vals):
	frame2=frame
    #frame2=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    ###pink marker starts
	lower_pink=list_of_min_vals[1]
	upper_pink=list_of_max_vals[1]
	mask=cv2.inRange(frame2,np.array(lower_pink),np.array(upper_pink))
	res=cv2.bitwise_and(frame2,frame2,mask=mask)
	#blur=cv2.cvtColor(res,cv2.COLOR_BGR2GRAY)
	#ret,thresh=cv2.threshold(blur,120,255,cv2.THRESH_BINARY)
	contours= cv2.findContours(mask.copy(),cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
	contours=contours[0]
	for k in range(0,len(contours)):
		c = contours[k]
		M = cv2.moments(c)
		area=M['m00']
		if area>0:
			cX = int((M['m10'] / M['m00']))
			cY = int((M['m01'] / M['m00']))
			#cv2.drawContours(frame,contours,k, (200,0,255),2)
    ### pink marker ends

	#### yellow marker starts
	lower_yellow=list_of_min_vals[0]
	upper_yellow=list_of_max_vals[0]
	mask2=cv2.inRange(frame2,np.array(lower_yellow),np.array(upper_yellow))
	#res2=cv2.bitwise_and(frame2,frame2,mask=mask2)
	#blur2=cv2.cvtColor(res2,cv2.COLOR_BGR2GRAY)
	#ret,thresh2=cv2.threshold(blur2,120,255,cv2.THRESH_BINARY)
	contours2= cv2.findContours(mask2.copy(),cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
	contours2=contours2[0]
	for k2 in range(0,len(contours2)):
		c2 = contours2[k2]
		M = cv2.moments(c2)
		area2=M['m00']
		if area2>0:
			cX2 = int((M['m10'] / M['m00']))
			cY2 = int((M['m01'] / M['m00']))
			#cv2.drawContours(frame,contours2,k2, (200,0,255),1)
			#cv2.putText(frame, 'head', (int(cX2), int(cY2)), cv2.FONT_ITALIC,0.5, (0,0,0), 2)
			#cv2.putText(frame, 'tail', (int(cX), int(cY)), cv2.FONT_ITALIC,0.5, (0,0,0), 2)

	#### yellow marker ends
	try:
		botX=(cX+cX2)/2
		botY=(cY+cY2)/2
		frame[botY,botX]=[255,255,255]
		cv2.line(frame,(int(botX),int(botY)),(int(x),int(y)),(0,255,255),2)
		cv2.line(frame,(cX2,cY2),(cX,cY),(0,255,255),2)
		cv2.imshow('hope',frame)
		cv2.waitKey(1)
		angle=orient([cX2,cY2],[cX,cY])
		pos=np.array([botX,botY,angle])
		return pos
	except:
		pass
	cv2.waitKey(1)	

def traverse(cap,target):
	x=target[0]
	y=target[1]
	center,list_of_max_vals,list_of_min_vals=bot_center(cap)
	botX=center[0]
	botY=center[1]
	while abs(botX-x)>50 or abs(botY-y)>50:
		ret,frame=cap.read()
		pos=trackBot(frame,x,y,list_of_max_vals,list_of_min_vals)
		botX=int(pos[0])
		botY=int(pos[1])
		#print botX,botY
		target_angle=orient([x,y],[botX,botY])
		diff=pos[2]-target_angle
		#print pos[2],target_angle,diff
		l=[]
		while abs(diff)>=30:
			if abs(diff)<=180:
				if diff>0:
					print pos[2],target_angle,'rotate',abs(diff),'left',botX-x, botY-y
					rotate_left()
				elif diff<0:
					print pos[2],target_angle,'rotate',abs(diff),'right',botX-x, botY-y
					rotate_right()
				#else:
					#print 'dont rotate'
			else:
				if diff>0:
					print pos[2],target_angle,'rotate',abs(360-diff),'right',botX-x, botY-y
					rotate_right()
				elif diff<0:
					print pos[2],target_angle,'rotate',abs(diff+360),'left',botX-x, botY-y
					rotate_left()

			ret,frame=cap.read()
			pos=trackBot(frame,x,y,list_of_max_vals,list_of_min_vals)
			botX=int(pos[0])
			botY=int(pos[1])
			#print botX,botY
			target_angle=orient([x,y],[botX,botY])
			diff=pos[2]-target_angle
			#print pos[2]
		forward()
'''
    while abs(pos[2])>5:
		if abs(pos[2])<90 and pos[2]<0:
			rotate('a')
		pos=trackBot(frame,x,y)
		ret,frame=cap.read()
		if cv2.waitKey(250)==27:
			break
'''
