
import Tkinter as tk
from templateDialog import *
from LabPalEngine import *

from PIL import ImageTk

TITLE_FONT = ("Calibri", 22, "bold")
BODY_FONT = ("Calibri", 14)

class ReadScreenDialog(templateDialog):
	def __init__(self, partask, *args,**kwargs):
		self.partask = partask # create a local copy of parent task
		self.finishedtask = None
		tkSimpleDialog.Dialog.__init__(self, *args,**kwargs)

	def body(self, master):

		namesinscope = self.partask.list_imageout()
		tk.Label(master, text="Read Screen Name:").grid(row=0)
		tk.Label(master, text="Snapshot:").grid(row=1)
		tk.Label(master, text="Units:").grid(row=2)

		self.nameentry = tk.Entry(master)
		self.nameentry.insert(0, "ScreenReader")

		self.datavar = tk.StringVar(master)
		self.datavar.set(namesinscope[0])
		self.dataentry = tk.OptionMenu(master, self.datavar, *namesinscope)

		self.unitentry = tk.Entry(master)
		self.unitentry.insert(0, "")

		self.nameentry.grid(row=0, column=1)
		self.dataentry.grid(row=1, column=1)
		self.unitentry.grid(row=2, column=1)
		return self.nameentry # initial focus


	def apply(self):
		snapname = self.datavar.get()
		for t in self.partask.tasks:
			if t.name == snapname:
				mycam = t.camera
		d1 = ScreenSelectDialog("Select the top left point on the screen", mycam, self)
		p1 = d1.point
		if p1 is not None:
			d2 = ScreenSelectDialog("Select the bottom right point on the screen", mycam, self)
			p2 = d2.point
			if p2 is not None:
				if p1[0] > p2[0]:
					xmin = p2[0]
					xmax = p1[0]
				else:
					xmin = p1[0]
					xmax = p2[0]

				if p1[1] > p2[1]:
					ymin = p2[1]
					ymax = p1[1]
				else:
					ymin = p1[1]
					ymax = p2[1]


def npboost(imin):
    baseline = (imin.real.astype(float) - np.min(imin))
    boosted = 255 * baseline/np.max(baseline)
    return boosted

class ScreenSelectDialog(templateDialog):

	def __init__(self, message, camera, *args,**kwargs):
		self.camera = camera
		self.message = message
		self.point = None
		tkSimpleDialog.Dialog.__init__(self, *args,**kwargs)

	def body(self, master):
		contframe = tk.Frame(self)

		camframe = tk.Frame(contframe)
		timerid = self.after(100, lambda:self.pack_cam_image(camframe) )
		camframe.pack(fill = "both")

		message = tk.Label(contframe, text=self.message, font=BODY_FONT)
		message.pack(side = "bottom")

		contframe.pack(fill = "both")

	def onmouse(self, event):
		self.point = [event.x, event.y]

	def pack_cam_image(self, master):
		for s in master.pack_slaves():
			s.destroy()
		camim = self.camera.getImage()
		sf = 300/float(camim.height)
		camscale = camim.scale(sf)
		if self.point is not None:
			circlelayer = DrawingLayer((camscale.width, camscale.height))
			circlelayer.circle(self.point, 5)
			camscale.addDrawingLayer(circlelayer)
			camscale = camscale.applyLayers()
		photo = ImageTk.PhotoImage(camscale.getPIL()) 
		label = tk.Label(master, image=photo) 
		label.camim = photo # keep a reference! 
		label.pack() #show the image
		label.bind('<Button-1>', self.onmouse)
		timerid = master.after(100, lambda:self.pack_cam_image(master) )


class DemoReadDialog(templateDialog):

	def __init__(self, point1, point2, camera, *args,**kwargs):
		self.camera = camera
		tkSimpleDialog.Dialog.__init__(self, *args,**kwargs)

	def body(self, master):
		contframe = tk.Frame(self)

		camframe = tk.Frame(contframe)
		timerid = self.after(100, lambda:self.pack_cam_image(camframe) )
		camframe.pack(fill = "both")

		message = tk.Label(contframe, text=self.message, font=BODY_FONT)
		message.pack(side = "bottom")

		contframe.pack(fill = "both")

	def onmouse(self, event):
		self.point = [event.x, event.y]

	def pack_cam_image(self, master):
		for s in master.pack_slaves():
			s.destroy()
		camim = self.camera.getImage()
		sf = 300/float(camim.height)
		camscale = camim.scale(sf)
		if self.point is not None:
			circlelayer = DrawingLayer((camscale.width, camscale.height))
			circlelayer.circle(self.point, 5)
			camscale.addDrawingLayer(circlelayer)
			camscale = camscale.applyLayers()
		photo = ImageTk.PhotoImage(camscale.getPIL()) 
		label = tk.Label(master, image=photo) 
		label.camim = photo # keep a reference! 
		label.pack() #show the image
		label.bind('<Button-1>', self.onmouse)
		timerid = master.after(100, lambda:self.pack_cam_image(master) )
