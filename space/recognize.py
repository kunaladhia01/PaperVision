import cv2
import numpy as np
import Tkinter as tk
from turtle import *
from PIL import Image
import math
import time
import random

cap = cv2.VideoCapture(0)
start = time.time()
#print start

pic_path = 'new2.jpg'
kernel = np.ones((5,5),np.uint8)
sw = 1920
sh = 1080

def inverter(image):
	image1 = gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	image1 = (255-image1)
	return image1
def nomotion():
	global start
	if time.time() - start > 5:
		start = time.time()
		return True
	return False

def define_lines():
	l = [1]
	rows = [0 for i in range(sw)]
	temp = Image.open(pic_path, 'r')
	pixels = temp.load()
	for i in range(temp.size[0]):
		for j in range(temp.size[1]):
			if pixels[i, j] <  100:
				#print str(i) + " " + str(j)
				rows[i] += 1
	for i in range(sw):
		if rows[i] > 400:
			found = False
			for x in l:
				if abs(x-i) < 20:
					found = True
					break
			if not found:
				l.append(i)
	#print l
	#print temp.size
	temp.close()
	return l

user_bullets = []

enemy_ships = [[] for i in range(10)]

setup( width = sw, height = sh, startx = None, starty = None)
Screen = Screen()
Screen.bgpic('bg.png')
title("PAPER VISION SPACE INVADERS")
char = Turtle()
char.ht()
char.penup()
dire = 0
char.goto(0,-500)
char.tilt(90)
char.fillcolor('#50ff00')
char.pencolor('#50ff00')
char.shape("turtle")
char.showturtle()

lines = []
count =0

def fire():
	global char
	global user_bullets
	too_many = False
	for thing in user_bullets:
		if thing.position()[1] < -300:
			too_many = True
			break
	if not too_many:
		#print 5
		b = Turtle()
		b.ht()
		b.penup()
		b.shape("circle")
		b.color("red")
		b.left(90)
		b.speed(0)
		b.goto(int(char.position()[0]), int(char.position()[1]))
		b.showturtle()
		user_bullets.append(b)
def k1():
	fire()

def k2():
	global dire
	dire = 0

def k3():
	global dire
	dire = 1

def k4():
	pass
onkey(k1, "Up")
onkey(k2, "Left")
onkey(k3, "Right")
onkey(k4, "Down")
listen()
while True:
	if not dire and char.position()[0] > -950:
		if len(user_bullets) < 2:
			char.back(3)
		elif len(user_bullets) < 4:
			char.back(5)
		else:
			char.back(7)

	if dire and char.position()[0] < 945:
		if len(user_bullets) < 2:
			char.forward(3)
		elif len(user_bullets) < 4:
			char.forward(5)
		else:
			char.forward(7)

	for u in user_bullets:
		u.forward(5)
		if u.position()[1] > 600:
			user_bullets.pop(user_bullets.index(u))
		
		else:
			for c in range(10):
				for d in enemy_ships[c]:
					if abs(d.position()[0]-u.position()[0]) < 50 and abs(d.position()[1]-u.position()[1]) < 20:
						enemy_ships[c][enemy_ships[c].index(d)].ht()
						enemy_ships[c].pop(enemy_ships[c].index(d))
						user_bullets[user_bullets.index(u)].ht()
						user_bullets.pop(user_bullets.index(u))
	if (nomotion()):
		
		frame = cv2.imread(pic_path)
		#_, frame = cap.read()
		frame = inverter(frame)
		opening = cv2.morphologyEx(frame, cv2.MORPH_OPEN, kernel)
		ret, opening2 = cv2.threshold(opening, 155, 255, cv2.THRESH_BINARY)
		opening2 = (255-opening2)
		width, height = opening2.shape[:2]
		#print width, height
		opening2 = cv2.resize(opening2, (0,0), fx=2, fy=1)
		resized_image = cv2.resize(opening2, (sw, sh))
		cv2.imwrite(pic_path, resized_image	)
		lines = define_lines()
		print len(lines)
		print count
		if count + 2 > len(lines):
			count = 0
		#crop
		tmp = Image.open(pic_path, 'r')
		tmp = tmp.crop((lines[count]+20, 1, lines[count+1] - 15, 1080))
		tmp.save('_0.png')
		tmp.close()

		#contours
		bw = cv2.imread('_0.png', 0)
		colour = cv2.imread
		#convert to black and white


		#threshold image
		ret, thresh = cv2.threshold(bw,0,5,0)
		#find contours
		im2, contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
		final = []
		for cnt in contours:
			if cv2.contourArea(cnt) > 12 and cv2.contourArea(cnt) < 3000:
				final.append(cnt)
		#print contours

		#print len(contours)
		#print len(contours[0])
		#print len(contours[0][0])
		#print final
		bw = (255)
		#convert coords to points
		
		coords = []
		cv2.drawContours(bw, contours, 0, (255, 255, 255) 	, 3)
		for cnt in final:
			M = cv2.moments(cnt)
			cx = int(M['m10']/M['m00'])
			cy = int(M['m01']/M['m00'])
			
			found = False
			for i in coords:
				if abs(i-cy) < 50:
					found = True
					break
			if not found:	
				coords.append(cy)
		

		for i in range(10):
			for p in enemy_ships[i]:
				p.goto(p.position()[0], p.position()[1] - 100)

		for e in enemy_ships[9]:
			loser = True
			colors  = ["yellow", "green", "purple", "blue", "orange", "brown", "black"]
			#char.color("black")
			#while True:
			#	pass	
			e.ht()
		enemy_ships.pop(9)

		new_row = []
		for f in coords:
			n = Turtle()
			n.speed(0)
			n.ht()
			n.tilt(270)
			#n.pensize(20)
			n.penup()
			n.goto(int(f*1.9 - 960), 500)
			n.shape("turtle")
			n.color("red")
			n.showturtle()
			new_row.append(n)

		enemy_ships.insert(0, new_row)
		#cv2.imwrite('xyza.png', bw)
		count += 1
		

mainloop()
