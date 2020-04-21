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

# Replace the URL with your own IPwebcam shot.jpg IP:port
url='http://10.251.80.184:8080/shot.jpg'


# Use urllib to get the image from the IP camera
imgResp = urllib.urlopen(url)

# Numpy to convert into a array
imgNp = np.array(bytearray(imgResp.read()),dtype=np.uint8)

# Finally decode the array to OpenCV usable format ;) 
img = cv2.imdecode(imgNp,-1)
	

tt = time.time()
def inverter(image):
	image1 = gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	image1 = (255-image1)
	return image1
def key_press(event):
    print event.char
    return event.char
    # Or whatever processing you might want.


#cap = cv2.VideoCapture(0)

kernel = np.ones((5,5),np.uint8)
#fgbg = cv2.bgsegm.createBackgroundSubtractorMOG()


#while(True):
	#ret, frame = vid.read()
	#img = inverter(frame)
	#opening = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)
while True:
	try:
		while True:
			#_, frame = cap.read(0)
			frame = img
			hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
			resized_image_0 = cv2.resize(hsv, (sw, sh))
			cv2.imwrite('ttt.png', resized_image_0)
			#frame = cv2.imread('rom.jpg', 0)
			#img = (255 - frame)
			img = inverter(frame)	
			opening = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)
			ret, opening2 = cv2.threshold(opening, 100, 255, cv2.THRESH_BINARY)
			opening2 = (255-opening2)
			width, height = opening2.shape[:2]
			print width, height
			opening2 = cv2.resize(opening2, (0,0), fx=2, fy=1)
			resized_image = cv2.resize(opening2, (sw, sh))
			cv2.imwrite('maze1.png', resized_image	)
			#cv2.waitKey(1) & 0xFF == ord('q')

			####################
			sizefit = sw,sh
			image = Image.open('maze1.png', 'r')
			image.thumbnail(sizefit, Image.ANTIALIAS)
			image.save('maze1.png', 'PNG')
			pix = image.load()


			setup( width = sw, height = sh, startx = None, starty = None)
			Screen = Screen()
			Screen.bgpic('maze1.png')
			title("Turtle Keys")
			move = Turtle()
#Color first 150 columns white
			move.ht()
			move.speed(0)
			move.pensize(300)
			move.ht()
			move.pencolor('#ffffff')
			move.fillcolor('#ffffff')
			move.penup()
			move.goto(-sw/2,sh/2)
			move.pendown()
			move.goto(-sw/2,-sh/2)
			move.penup()
			move.goto(sw/2,sh/2)
			move.pendown()
			move.goto(sw/2,-sh/2)
			move.penup()
#Start Circle
			move.goto(-sw/2+50,sh/2-120)
			move.pendown()
			move.fillcolor('#5000ff')
			move.pencolor('#5000ff')
			move.pensize(5)
			move.circle(40)
			move.penup()
			move.goto(-sw/2+33,sh/2-80)
			move.write("START")
			move.shape("turtle")
			move.fillcolor('#50ff00')
			move.pencolor('#50ff00')
			move.goto(-sw/2+45,sh/2-90)
			move.pendown()
#Finish Circle
			move.penup()
			move.goto(sw/2-50,-sh/2+120)
			move.pendown()
			move.fillcolor('#b631a3')
			move.pencolor('#b631a3')
			move.pensize(5)
			move.circle(40)
			move.penup()
			move.goto(sw/2-68,-sh/2+162)
			move.write("FINISH")
			move.fillcolor('#50ff00')
			move.pencolor('#50ff00')
			move.goto(-sw/2+45,sh/2-90)
			move.fillcolor('#bd7f1f')
			move.pendown()
			move.showturtle()
			for i in range(150):
				for j in range(sh):
					pix[i,j] = 255
					pix[sw-i-1, j] = 255
			def winScreen():
				move.speed(10)
				move.pensize(1920)
				move.goto(-sw/2, sh/2)
				move.fillcolor('#50ff00')
				move.goto(sw/2,-sh/2)
				move.ht()
				move.goto(-150,0)
				move.pencolor('#ffffff')
				move.pensize(10)
				move.write("You WIN!", font=("Arial", 36, "bold"))
			def loseScreen():
				move.speed(10)
				move.pensize(1920)
				move.goto(-sw/2, sh/2)
				move.fillcolor('#bd7f1f')
				move.goto(sw/2,-sh/2)
				move.ht()
				move.goto(-150,0)
				move.pencolor('#ffffff')
				move.pensize(10)
				move.write("You WIN!", font=("Arial", 36, "bold"))
			def checkFinish():
				#if it reaches end
				xxx = (move.position()[0]-sw/2+50)
				yyy = (move.position()[1]+sh/2-155)
				dist = math.sqrt(xxx**2+yyy**2)
				print xxx,yyy
				if dist<50:
					winScreen()	
					#screen.destroy()
			def k1():
				checkFinish()
				currentpos = move.position()
				currentang = move.heading()*math.pi/180
				print currentpos
				if pix[currentpos[0]+5*math.cos(currentang)+sw/2, -(currentpos[1]+5*math.sin(currentang))+sh/2]>100:
					move.forward(5)
				
			#	if pix[currentpos[0]+5*math.cos(currentang)+1920, currentpos[1]+5*math.sin(currentang)+1080]>100:
			p = False

			def k2():
			    move.left(10)
			def k3():
			    move.right(10)

			def k4():
				checkFinish()				
				currentpos = move.position()
				currentang = move.heading()*math.pi/180
				print currentpos
				if pix[currentpos[0]-5*math.cos(currentang)+sw/2, -(currentpos[1]-5*math.sin(currentang))+sh/2]>100:
					move.back(5)
			onkey(k1, "Up")
			onkey(k2, "Left")
			onkey(k3, "Right")
			onkey(k4, "Down")

			if p:
				break
			listen()
			mainloop()

	except KeyboardInterrupt:
		pass

