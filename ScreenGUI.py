
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
		self.name = self.nameentry.get()
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

				rd = DemoReadDialog([xmin,ymin], [xmax,ymax], mycam, self)
				if rd.finishedtask is not None:
					self.finishedtask = ImageTask(self.name, 0, snapname , IMT_readdigits, [xmin,ymin],[xmax,ymax])


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
		self.point = [event.x/self.sf, event.y/self.sf]

	def pack_cam_image(self, master):
		for s in master.pack_slaves():
			s.destroy()
		camim = self.camera.getImage()
		self.sf = 300/float(camim.height)
		camscale = camim.scale(self.sf)
		if self.point is not None:
			circlelayer = DrawingLayer((camscale.width, camscale.height))
			circlelayer.circle([self.point[0]*self.sf,self.point[1]*self.sf], 5, color = (255,0,0))
			camscale.addDrawingLayer(circlelayer)
			camscale = camscale.applyLayers()
		photo = ImageTk.PhotoImage(camscale.getPIL()) 
		label = tk.Label(master, image=photo) 
		label.camim = photo # keep a reference! 
		label.pack() #show the image
		label.bind('<Button-1>', self.onmouse)
		timerid = master.after(200, lambda:self.pack_cam_image(master) )


class DemoReadDialog(templateDialog):

	def __init__(self, point1, point2, camera, *args,**kwargs):
		self.finishedtask = None
		self.point1 = point1
		self.point2 = point2
		self.camera = camera
		tkSimpleDialog.Dialog.__init__(self, *args,**kwargs)

	def body(self, master):
		contframe = tk.Frame(self)

		self.message = tk.Label(contframe, text="hello", font=BODY_FONT)
		self.message.pack(side = "bottom")

		camframe = tk.Frame(contframe)
		timerid = self.after(200, lambda:self.pack_cam_image(camframe) )
		camframe.pack(fill = "both")

		contframe.pack(fill = "both")

	def apply(self):
		self.finishedtask = 1


	def pack_cam_image(self, master):
		for s in master.pack_slaves():
			s.destroy()
		camim = self.camera.getImage()
		camim = camim.regionSelect(self.point1[0], self.point1[1], self.point2[0], self.point2[1])
		sf = 300/float(camim.height)
		camscale = camim.scale(sf)
		photo = ImageTk.PhotoImage(camscale.getPIL()) 
		label = tk.Label(master, image=photo) 
		label.camim = photo # keep a reference! 
		label.pack() #show the image
		digs = IMT_readdigits(camscale,[0,0],[camscale.width,camscale.height])
		self.message["text"] = digs
		timerid = master.after(200, lambda:self.pack_cam_image(master) )
