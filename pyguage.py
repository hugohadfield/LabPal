
from SimpleCV import *
import time

def guage_angle(threshold,imin):
	lines = imin.findLines(threshold=threshold, minlinelength=20)
	return lines

if __name__ == "__main__":
	cam = Camera(1)
	while 1:
		imin = cam.getImage().regionSelect (260, 211, 366, 303)
		#dl = imin.getDrawingLayer() 
		lines =  guage_angle(40,imin)
		print lines[0].angle()
		time.sleep(0.1)