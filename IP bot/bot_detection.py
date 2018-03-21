import numpy as np
import cv2
import math
#from color_track_fun_mouse_events import *

refPt = []
cropping = False
 
def click_and_crop(event, x, y, flags, param):
	# grab references to the global variables
	global refPt, cropping,image
 
	# if the left mouse button was clicked, record the starting
	# (x, y) coordinates and indicate that cropping is being performed

	if event == cv2.EVENT_LBUTTONDOWN:
		refPt = [(x, y)] # reference point for cropping
		cropping = True
 
	# check to see if the left mouse button was released
	elif event == cv2.EVENT_LBUTTONUP:
		# record the ending (x, y) coordinates and indicate that
		# the cropping operation is finished
		refPt.append((x, y))
		cropping = False
 
		# drawing a rectangle around the region of interest
		cv2.rectangle(image, refPt[0], refPt[1], (0, 255, 0), 2)
		cv2.imshow("image", image)

def find_shape(c):
    shape = "unidentified"
    peri = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, 0.04 * peri, True)
    if len(approx) == 3 :
        shape = "Triangle"
    elif len(approx) ==4 :
        shape = "4-sided"
    else:
        shape = "Circle"
    return shape

def angle(pt1,pt2): # pt1 is the source and pt2 is destination pt1-->pt2
	[cX,cY]   = pt1
	[cX2,cY2] = pt2
	theta = math.atan2((cY2-cY),(cX2-cX))*(180/3.1414) # in degrees
	if theta<0:
		theta+=360
	return theta	

def bot_center(cap):
    _,image=cap.read()
    flag1 = 0
    flag2 = 0
    # load the image, clone it, and setup the mouse callback function
    #image = cv2.imread(im_file_name)
    num_of_unique_colors = 2 # yellow and pink	
    list_of_min_vals=[] # first yellow then pink	
    list_of_max_vals=[] # first yellow then pink
    list_of_min_vals_2=[] # first yellow then pink	
    list_of_max_vals_2=[] # first yellow then pink
    for i in xrange(num_of_unique_colors):	
        clone = image.copy()
        cv2.namedWindow("image")
        cv2.setMouseCallback("image", click_and_crop)
            
        # keep looping until the 'q' key is pressed
        while True:
            # display the image and wait for a keypress
            cv2.imshow("image", image)
            key = cv2.waitKey(1) & 0xFF

            # if the 'r' key is pressed, reset the cropping region
            if key == ord("r"):
                image = clone.copy()

            # if the 'c' key is pressed, break from the loop
            elif key == ord("c"):
                break
            
        # if there are two reference points, then crop the region of interest
        # from the image and display it
        if len(refPt) == 2:
            roi = clone[refPt[0][1]:refPt[1][1], refPt[0][0]:refPt[1][0]]
            max_val_R = roi[:,:,2].max() # max val of red channel in roi
            max_val_G = roi[:,:,1].max() # max val of green channel in roi
            max_val_B = roi[:,:,0].max() # max val of blue channel in roi

            min_val_R = roi[:,:,2].min() # min val of red channel in roi
            min_val_G = roi[:,:,1].min() # min val of green channel in roi
            min_val_B = roi[:,:,0].min() # min val of blue channel in roi
            print "max vals"
            print str(max_val_R)+","+str(max_val_G)+","+str(max_val_B)
            print "min vals"
            print str(min_val_R)+","+str(min_val_G)+","+str(min_val_B)
            cv2.imshow("roi", roi)
            cv2.waitKey(0)
        cv2.destroyAllWindows()
        list_of_min_vals.append([min_val_B-10,min_val_G-10,min_val_R-10]) # [yellow,pink]	
        list_of_max_vals.append([max_val_B+10,max_val_G+10,max_val_R+10]) # [yellow,pink]
    delta_row = abs(refPt[0][0] - refPt[1][0])
    delta_col = abs(refPt[0][1] - refPt[1][1])
    #### pink marker ######################
    lower_pink=np.array(list_of_min_vals[1])
    upper_pink=np.array(list_of_max_vals[1])

    mask=cv2.inRange(image,lower_pink,upper_pink)
    kernel = np.ones((5,5),np.uint8)
    mask = cv2.dilate(mask,kernel,iterations = 1)
    #cv2.imshow('pink',mask)
    contours, hierarchy = cv2.findContours(mask.copy(),cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    l=[]
    for k in range(0,len(contours)):
        c = contours[k]
        M = cv2.moments(c)
        area=M['m00']
        if area>=0 and area<100000:
            print area
            cX = int((M['m10'] / M['m00']))
            cY = int((M['m01'] / M['m00']))
            l.append([cX,cY])
            shape = find_shape(contours[k])
            roi = image[(cY-delta_row/2):(cY+delta_row/2),(cX-delta_col/2):(cX+delta_col/2)]
            #try:
                #cv2.imshow('pink roi',roi)
            #except:
                #pass		
            #cv2.drawContours(image,contours,k, (200,0,255),2)	
            #cv2.putText(image, 'tail', (int(cX), int(cY)), cv2.FONT_ITALIC,0.5, (0,0,0), 2)

    ########################################

    #### yellow marker #####################	

    lower_yellow=np.array(list_of_min_vals[0])
    upper_yellow=np.array(list_of_max_vals[0])

    mask2=cv2.inRange(image,lower_yellow,upper_yellow)
    kernel = np.ones((5,5),np.uint8)
    mask2 = cv2.dilate(mask2,kernel,iterations = 1)
    contours2, hierarchy2 = cv2.findContours(mask2.copy(),cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    #cv2.imshow('yellow',mask2)
    l2=[]
    for k2 in range(0,len(contours2)):
        c2 = contours2[k2]
        M = cv2.moments(c2)
        area2=M['m00']
        print area2
        if area2>=0 and area2<100000:	
            cX2 = int((M['m10'] / M['m00']))
            cY2 = int((M['m01'] / M['m00']))
            l2=[cX2,cY2]
            shape = find_shape(contours2[k2])
            roi2 = image[(cY2-delta_row/2):(cY2+delta_row/2),(cX2-delta_col/2):(cX2+delta_col/2)]
            #try:
                # cv2.imshow('yellow roi',roi2)
            # except:
                #pass		
            #cv2.drawContours(image,contours2,k2, (200,0,255),2)
            #cv2.putText(image, 'head', (int(cX2), int(cY2)), cv2.FONT_ITALIC,0.5, (0,0,0), 2)		

    ##########################################
    center = (int((cX2+cX)/2),int((cY2+cY)/2))	
    #cv2.imshow('hope',image)
    #navigate(center,dest,list_of_max_vals,list_of_min_vals)
    # theta > 0 : anticlockwise rotation
    # theta < 0 : clockwise rotation
    #q=cv2.waitKey(10) & 0xff	
    #if q == 27:
    #    break	
    print 'hey'		
    return center,list_of_max_vals,list_of_min_vals
    #cap.release()
    #cv2.destroyAllWindows()		




