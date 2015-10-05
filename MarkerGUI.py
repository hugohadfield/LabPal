
import Tkinter as tk
import tkSimpleDialog
import math
from SimpleCV import Camera, Image
import numpy as np
from PIL import ImageTk
from LabPalEngine import *

BODY_FONT = ("Comic Sans", 14)


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
		self.marker_blob(newim, self.point)

	def pack_cam_image(self, master):
		for s in master.pack_slaves():
			s.destroy()
		camim = self.camera.getImage()
		sf = 300/float(camim.height)
		newim = camim.scale(sf)
		photo = ImageTk.PhotoImage(newim.getPIL()) 
		label = tk.Label(master, image=photo) 
		label.camim = photo # keep a reference! 
		label.pack() #show the image
		label.bind('<Button-1>', self.onmouse)
		if self.markercolor is not None:
			IMT_find_col(newim, self.markercolor)
		timerid = master.after(100, lambda:self.pack_cam_image(master) )

	def marker_blob(self, imin, p):
		self.markercolor = imin[p]

if __name__ == "__main__":
	root = tk.Tk()
	MarkerSelectDialog("Select a colored marker fixed to the scale", Camera(1), root)
