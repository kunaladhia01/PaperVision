import cv2
import numpy as np
import Tkinter as tk
from turtle import *
from PIL import Image
import math
import time
sw = 1920
sh = 1080
import urllib
from sympy import *
import matplotlib.pyplot as plt
from math import log

def inverter(image):
	image1 = gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	image1 = (255-image1)
	return image1

def key_press(event):
    return event.char

def determine_eq(order, arr):
	matrix = [[0 for x in range(order + 2)] for x in range (order + 1)]
	for row in range (0, order+1):
		matrix[row][order+1] = arr[row][1]
		matrix[row][order] = 1
	for row in range(0, order+1):
		for column in range (0, order):
	    		matrix[row][column] = arr[row][0]**(order-column)
    
    	M = Matrix(matrix)
	M = M.rref()
	return M[0].col(-1)


def getImg():
	try:
		while True:
		# Replace the URL with your own IPwebcam shot.jpg IP:port
			url='http://10.251.80.184:8080/shot.jpg'


			# Use urllib to get the image from the IP camera
			imgResp = urllib.urlopen(url)

			# Numpy to convert into a array
			imgNp = np.array(bytearray(imgResp.read()),dtype=np.uint8)

			kernel = np.ones((5,5),np.uint8)
			# Finally decode the array to OpenCV usable format ;) 
			img = cv2.imdecode(imgNp,-1)
	
			img = inverter(img)	
			opening = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)
			#opening = (255-opening)
			ret, opening2 = cv2.threshold(opening, 120, 255, cv2.THRESH_BINARY)
			opening2 = cv2.cvtColor(opening2,cv2.COLOR_GRAY2RGB)
			height, width = opening2.shape[:2]
			cv2.line(opening2,(width/2,0),(width/2,height),(255,255,0),5)
			cv2.line(opening2,(0,height/2),(width,height/2),(255,255,0),5)
			for i in range(1,17):
				cv2.line(opening2, (width/2+60*i, 0), (width/2+60*i,height), (0,255,255), 1)
				cv2.line(opening2, (width/2-60*i, 0), (width/2-60*i,height), (0,255,255), 1)  
			for i in range(1,10):
				cv2.line(opening2, (0, height/2+60*i), (width, height/2+60*i), (0,255,255), 1)
				cv2.line(opening2, (0, height/2-60*i), (width, height/2-60*i), (0,255,255), 1)
			cv2.imshow('img',opening2)
			cv2.waitKey(1)
	except KeyboardInterrupt:
		print "ASD"
    		return opening2
finalimg = getImg()
cv2.imwrite('final.jpg', finalimg)


points = []

leftside = True
rightside = True
for i in range(1,900,60):
	if rightside:
		for j in range(0,1080):
			if str(finalimg[j,960+i])=="[255 255 255]":
				points.append((i/60.0,-j/60.0+9))
				break
			#if j==1079:
				#rightside = False
	if leftside:
		for j in range(0,1080):
			if str(finalimg[j,960-i])=="[255 255 255]":
				points.append((-i/60.0,-j/60.0+9))
				break
			#if j==1079:
				#leftside = False
y = determine_eq(len(points)-1, points)
testList2 = [(elem1, log(elem2)) for elem1, elem2 in points]
plt.scatter(*zip(*testList2))
plt.show()
counter = len(points)
for i in y:
	counter-=1
	if abs(i) < 0.05:
		continue	
	print str(i) + "x^" + str(counter) 
	
