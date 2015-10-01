
import Tkinter as tk
import tkSimpleDialog
import math
from SimpleCV import Camera, Image
import numpy as np
from PIL import ImageTk

BODY_FONT = ("Comic Sans", 14)

def npboost(imin):
    baseline = (imin.real.astype(float) - np.min(imin))
    boosted = 255 * baseline/np.max(baseline)
    return boosted

def cartdist(p1,p2):
	return math.sqrt( (p1[0] - p2[0])*(p1[0] - p2[0]) + (p1[1] - p2[1])*(p1[1] - p2[1]))

def marker_blob(imin, p):
	xvals = np.arange(0,imin.width)
	xsqr = np.square( (xvals - p[0]) )
	yvals = np.arange(0,imin.height)
	ysqr = np.square( (yvals - p[1]) )

	fullxsqr = np.transpose( np.tile( xsqr, (imin.height,1) ) )
	fullysqr = np.tile( ysqr, (imin.width,1) )  
	dist = npboost( np.sqrt(fullysqr + fullxsqr) )
	coldist = imin.colorDistance( imin[p] )

	lolout = Image( npboost(   dist + np.squeeze(np.dsplit( coldist.getNumpy(), 3)[0] )  ) )
	blobs = lolout.stretch(0,20).invert().findBlobs()
	lolout.stretch(0,20).invert().show()

class MarkerSelectDialog(tkSimpleDialog.Dialog):

	def __init__(self, message, camera, *args,**kwargs):
		self.camera = camera
		self.message = message
		self.markercolor = None
		self.centroid = None
		tkSimpleDialog.Dialog.__init__(self, *args,**kwargs)

	def body(self, master):
		contframe = tk.Frame(self)

		camframe = tk.Frame(contframe)
		timerid = self.after(100, lambda:self.pack_cam_image(camframe) )
		camframe.pack(fill = "both")

		message = tk.Label(contframe, text=self.message, font=BODY_FONT)
		message.pack(side = "bottom")

		contframe.pack(fill = "both")

	def buttonbox(self):
		box = tk.Frame(self)
		w = tk.Button(box, text="Cancel", font = BODY_FONT, width=10, command=self.cancel)
		w.pack(padx=5, pady=5)
		self.bind("<Escape>", self.cancel)
		box.pack()

	def onmouse(self, event):
		self.point = [event.x, event.y]
		print self.point
		self.extract_marker()

	def extract_marker(self):
		camim = self.camera.getImage()
		sf = 300/float(camim.height)
		newim = camim.scale(sf)
		marker_blob(newim, self.point)

	def pack_cam_image(self, master):
		for s in master.pack_slaves():
			s.destroy()
		camim = self.camera.getImage()
		sf = 300/float(camim.height)
		photo = ImageTk.PhotoImage(camim.scale(sf).getPIL()) 
		label = tk.Label(master, image=photo) 
		label.camim = photo # keep a reference! 
		label.pack() #show the image
		label.bind('<Button-1>', self.onmouse)
		timerid = master.after(100, lambda:self.pack_cam_image(master) )


if __name__ == "__main__":
	root = tk.Tk()
	MarkerSelectDialog("Select a colored marker fixed to the scale", Camera(0), root)