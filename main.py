#!/usr/bin/env python2

import cv2
from Tkinter import *
import tkFont as font
import tkFileDialog
from PIL import Image
from PIL import ImageTk
import numpy as np

WIDTH = 640
HEIGHT = 480

points = []
priorPoints = []
contour_color = [255,255,0]

area = 0
region_area = 0
window = None
areaText = None

class Point:
	x = 0
	y = 0

	def __init__(self,a,b):
	    self.x = a
	    self.y = b

def calculateArea():
  n = 0
  j = len(points)-1

  for i in range(0,len(points)):
  	n += (points[j].x+points[i].x)*(points[j].y-points[i].y)
  	j = i

  return abs(n*.5)

def getPoint(evt):
	points.append(Point(evt.x,evt.y))
	priorPoints.append(Point(evt.x,evt.y))
	arr = np.array([[e.x, e.y] for e in priorPoints]) 
	cv2.fillConvexPoly(cvimage,arr,contour_color,10)
	if len(priorPoints) >= 2:
		priorPoints.pop(0)
	image = Image.fromarray(cvimage)
	image = ImageTk.PhotoImage(image)
	window.configure(image=image)
	window.image = image	

def getArea(evt):
	global area, areaText

	region_area = calculateArea()
	area += region_area;

	areaText.delete('1.0', END)
	areaText.insert(END,"Region Area: " + str(region_area) + "\n\n")
	areaText.insert(END,"Total Area: " + str(area))
	
	points[:] = []
	priorPoints[:] = []

def get_image():
	global window, image, cvimage, areaText, width, height, bigfont, area, region_area

	path = tkFileDialog.askopenfilename()

	if len(path) > 0:
		area = 0
		region_area = 0
		image = cv2.imread(path)
		image = cv2.resize(image, (WIDTH, HEIGHT)) 
		image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
		cvimage = image
		image = Image.fromarray(image)
		image = ImageTk.PhotoImage(image)

		if window == None and areaText == None:
			window = Label(image=image)
			window.image = image
			window.place(x=30,y=30)
			window.bind("<Button-1>", getPoint)
			window.bind("<Button-3>", getArea)

			areaText = Text(height = 4, width=25, font=bigfont)
			areaText.insert(END,"Region Area: " + str(region_area) + "\n\n")
			areaText.insert(END,"Total Area: " + str(area))
			areaText.place(x=width-400,y=height/3)
		else:
			window.configure(image=image)
			window.image = image

			areaText.delete('1.0', END)
			areaText.insert(END,"Region Area: " + str(region_area) + "\n\n")
			areaText.insert(END,"Total Area: " + str(area))


root = Tk()
root.title("Image Area Calculator")

width = root.winfo_screenwidth()
height = root.winfo_screenheight()
helv36 = font.Font(family="helvetica", size=36)
bigfont = font.Font(family="helvetica", size=20)

btn = Button(root, text="Open image", font=helv36, command=lambda:get_image())
btn.place(x=width-400,y=100)

text = Text(height = 10, width = 40, font=bigfont)
text.insert(END,"Image Area Calculator\n\n")
text.insert(END,"Image Size: 640x480")
text.place(x=width-400,y=height-300)
text.config(state=DISABLED)

root.mainloop()