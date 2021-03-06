'''
loading the dependencies
'''
import numpy as np
import cv2
from visibility_graph import *
from dijstra import *
import numpy as np
import cv2
import math

'''
global variables
'''
refPt = []
cropping = False
inf = float("9e999")
 
def click_and_crop(event, x, y, flags, param):
	# grab references to the global variables
	global refPt, cropping
 
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

'''
The below give function takes input as a image and returns a path from source(brown) to destination(green)
by visiting all yellow objects in the image
'''
def part1(image): 
	clone = image.copy()
	image2 = image
	cv2.namedWindow("image")
	cv2.setMouseCallback("image", click_and_crop)
	list_of_min_vals= []
	list_of_max_vals =[] 
	num_of_unique_colors = 5 #(white(obstacles), bot(brown), objects(yellow), end(green))
	# keep looping until the 'q' key is pressed
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
			if i==0:
				image = roi
				continue		
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
	
		list_of_min_vals.append([min_val_B-10,min_val_G-10,min_val_R-10]) # [yellow,pink]	
		list_of_max_vals.append([max_val_B+10,max_val_G+10,max_val_R+10]) # [yellow,pink]
		cv2.destroyAllWindows()
	
	'''
	 initializing variables
	'''
	obstacles = []
	nodes = []
	lines = []
	nrow,ncol,_ = image.shape
	'''
	brown object  ---> assume to be bot
	'''
	lower_brown=np.array(list_of_min_vals[0])
	upper_brown=np.array(list_of_max_vals[0])

	mask=cv2.inRange(image,lower_brown,upper_brown)
	kernel = np.ones((5,5),np.uint8)
	mask = cv2.dilate(mask,kernel,iterations = 1)
	cv2.imshow('brown',mask)
	contours_brw,hierarchy = cv2.findContours(mask.copy(),cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

	for i in xrange(len(contours_brw)):
		x,y,w,h = cv2.boundingRect(contours_brw[i])
		if w*h>1000:
			nodes.append((x+w/2,y+h/2))
	#########################################

	'''
	obstacles ---> to be avoided
	'''
	lower_white=np.array(list_of_min_vals[1])
	upper_white=np.array(list_of_max_vals[1])

	mask=cv2.inRange(image,lower_white,upper_white)
	kernel = np.ones((5,5),np.uint8)
	mask = cv2.dilate(mask,kernel,iterations = 15)
	cv2.imshow('obs',mask)
	contours_ob,hierarchy = cv2.findContours(mask.copy(),cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE) 
	for i in xrange(len(contours_ob)):
		x,y,w,h = cv2.boundingRect(contours_ob[i])
		rect = cv2.minAreaRect(contours_ob[i])
		if abs(rect[-1])%90 !=0:
			box = cv2.cv.BoxPoints(rect)
			box = np.int0(box)
			obstacles.append(tuple(box[0]))
			obstacles.append(tuple(box[1]))
			obstacles.append(tuple(box[2]))
			obstacles.append(tuple(box[3]))
			nodes.append(tuple(box[0]))
			nodes.append(tuple(box[1]))
			nodes.append(tuple(box[2]))
			nodes.append(tuple(box[3]))
			lines.append([tuple(box[0]),tuple(box[1])])
			lines.append([tuple(box[1]),tuple(box[2])])
			lines.append([tuple(box[2]),tuple(box[3])])
			lines.append([tuple(box[3]),tuple(box[0])])
			lines.append([tuple(box[0]),tuple(box[2])])
			lines.append([tuple(box[1]),tuple(box[3])])
			#print [tuple(box[0]),tuple(box[1])]
		#print rect

		#x,y,w,h = box
		if y>5 :
			obstacles.append((x,y))
			obstacles.append((x+w,y))
			nodes.append((x,y))
			nodes.append((x+w,y))
		if y+h<ncol-15 :		
			obstacles.append((x+w,y+h))
			obstacles.append((x,y+h))
			nodes.append((x+w,y+h))
			nodes.append((x,y+h))
		lines.append([(x,y),(x+w,y)])
		lines.append([(x+w,y),(x+w,y+h)])
		lines.append([(x+w,y+h),(x,y+h)])
		lines.append([(x,y+h),(x,y)])
		lines.append([(x,y),(x+w,y+h)])
		lines.append([(x+w,y),(x,y+h)])

	#########################################	

	'''
	 yellow object  ---> objects to be visited
	''' 
	list_of_squares = []
	list_of_triangles = []
	lower_yellow=np.array(list_of_min_vals[2])
	upper_yellow=np.array(list_of_max_vals[2])

	mask=cv2.inRange(image,lower_yellow,upper_yellow)
	kernel = np.ones((5,5),np.uint8)
	mask = cv2.dilate(mask,kernel,iterations = 1)
	cv2.imshow('yellow',mask)
	contours_yel,hierarchy = cv2.findContours(mask.copy(),cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
	# appending the nodes 
	for i in xrange(len(contours_yel)):
		M = cv2.moments(contours_yel[i])
		cX = int((M['m10'] / M['m00']))
		cY = int((M['m01'] / M['m00']))
		shape = find_shape(contours_yel[i])
		if shape == '4-sided':
			list_of_squares.append((cX,cY))
		else:
			list_of_triangles.append((cX,cY))	
		x,y,w,h = cv2.boundingRect(contours_yel[i])
		if w*h>1000:
			nodes.append((cX,cY))
	#########################################

	'''
	green object  ---> final destination
	'''
	lower_green=np.array(list_of_min_vals[3])
	upper_green=np.array(list_of_max_vals[3])

	mask=cv2.inRange(image,lower_green,upper_green)
	kernel = np.ones((5,5),np.uint8)
	mask = cv2.dilate(mask,kernel,iterations = 1)
	cv2.imshow('green',mask)
	contours_yel,hierarchy = cv2.findContours(mask.copy(),cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
	# appending the nodes 
	for i in xrange(len(contours_yel)):
		x,y,w,h = cv2.boundingRect(contours_yel[i])
		if w*h>1000:
			nodes.append((x+w/2,y+h/2))
	#########################################

	list_of_neighbours = [] # stores the list of neighbours(where the first node in each neighbour is the primary node or should be the key of the graph)
	for pt in nodes:
		list_of_neighbours.append(finding_neighbours(pt,nodes,lines))

	temp = [(),inf]
	graph={}
	for neighbour in list_of_neighbours:
		graph[neighbour[0]] = neighbour[1:]
		graph[neighbour[0]].extend(temp) 
	
	'''
	the below written code finds a path between the start and end node via all other objects using nearest neighbour
	paradigm
	'''
	flip_flag = 1 # for alternate picks, if flag = 0, we need to pick square else we need to pick triangle
	alternate_flag = 0
	visited_list = []
	right_path = []
	final_path = []
	start_node = nodes[0]
	visited_list.append(start_node)
	end_node = nodes[-1]
	#print end_node
	count = 9 # number of nodes I want to visit before visiting the end node
	if alternate_flag==0: # no need to pick alternate shape
		for i in xrange(10):
			if count == 0:
				#print 'hey'
				#destination = end_node
				path,total_cost = dijstra_short_path(start_node,end_node,graph)
				path.reverse()
				final_path.extend(path)
				break
			min_dist = 100000
			for node_2 in nodes[1:]:
				if node_2 in obstacles: continue # we dont have to visit the obstacles 
				if node_2 in visited_list: continue # donot visit already visited nodes
				if node_2 == end_node: continue
				path,total_cost = dijstra_short_path(start_node,node_2,graph)
				path.reverse()
				if min_dist>total_cost:
					min_dist = total_cost
					right_path = path
			count-=1				
			final_path.extend(right_path[:-1])
			start_node = right_path[-1]
			visited_list.append(start_node)	
			# again rebuilding the graph because it gets modified while doing path planning(dont know why yet)
			temp = [(),inf]
			graph={}
			for neighbour in list_of_neighbours:
				graph[neighbour[0]] = neighbour[1:]
				graph[neighbour[0]].extend(temp)		
	#print list_of_triangles == list_of_squares
	if alternate_flag == 1: # we need to visit alternate shapes while traversing from start to end node
		for i in xrange(10):
			if count == 0:
				#print 'hey'
				#destination = end_node
				path,total_cost = dijstra_short_path(start_node,end_node,graph)
				path.reverse()
				final_path.extend(path)
				break
			min_dist = 100000
			for node_2 in nodes[1:]:
				if node_2 in obstacles: continue # we dont have to visit the obstacles 
				if node_2 in visited_list: continue # donot visit already visited nodes
				if node_2 == end_node: continue		
				if flip_flag == 0 and (node_2 in list_of_triangles):
					continue
				if flip_flag == 1 and (node_2 in list_of_squares):
					continue
				path,total_cost = dijstra_short_path(start_node,node_2,graph)
				path.reverse()
				if min_dist>total_cost:
					min_dist = total_cost
					right_path = path
					destination_node = node_2

			#if count ==9: # as the closest node to the start can be any node hence for first iteration we dont see its shape
				#if destination_node in list_of_squares: flip_flag = 0	
				#if destination_node in list_of_triangles: flip_flag = 1	
			count-=1				
			final_path.extend(right_path[:-1])
			start_node = right_path[-1]
			visited_list.append(start_node)	
			if (destination_node in list_of_squares) or (destination_node in list_of_triangles):
				flip_flag = abs(flip_flag-1) # update the flag to pick alternate object in next iteration
				#print flip_flag
			# rebuilding the graph as the graph gets changed
			temp = [(),inf]
			graph={}
			for neighbour in list_of_neighbours:
				graph[neighbour[0]] = neighbour[1:]
				graph[neighbour[0]].extend(temp)		


	'''
	the following code draws the visibility graph on the image(visualization)
	'''	
	for neighbour in list_of_neighbours:
		if len(neighbour)==0:
			continue
		first_point = neighbour[0]
		for point in neighbour[1:]:
			second_point = point
			cv2.line(image,first_point,second_point,(0,0,255),2)
	
	visit = []	
	#print final_path
	temp = final_path[0]

	for i in xrange(len(final_path)-1):
		if i+1==len(final_path):
			break
		if final_path[i+1]==temp:
			final_path.remove(final_path[i])	
		temp = final_path[i+1]			
	counter = 0
	for i in xrange(len(final_path)):
		cv2.putText(image2,str(counter),final_path[i], cv2.FONT_HERSHEY_SIMPLEX, 1,(255,0,0),2)	
		visit.append(final_path[i])	
		counter+=1
	cv2.imshow('image',image2)
	cv2.waitKey(0)
	cv2.destroyAllWindows()
	l = []
	for i in final_path:
		if (i not in list_of_triangles) and (i not in list_of_squares):
			l.append((i,0))
		if i in list_of_squares: l.append((i,1))
		if i in list_of_triangles: l.append((i,2))
	return l
	#return final_path,list_of_squares,list_of_triangles


if __name__ == '__main__':
	image = cv2.imread('Capture.JPG')
	image = cv2.resize(image,(649, 647))
	print 'crop out the start marker, white obstacle, yellow objects and end marker respectively'
	final_path,list_of_squares,list_of_triangles = part1(image)
	l = []
	for i in final_path:
		if (i not in list_of_triangles) and (i not in list_of_squares):
			l.append([i,0])
		if i in list_of_squares: l.append([i,1])
		if i in list_of_triangles: l.append([i,2])
	print l
	#print list_of_squares,list_of_triangles
	#print 'crop out the head marker and tail marker of the bot respectively'
	#main(final_path)	
	#print 'work done'	
