
import Tkinter as tk
from templateDialog import *
from LabPalEngine import *
from ScreenGUI import *

from PIL import ImageTk

TITLE_FONT = ("Calibri", 22, "bold")
BODY_FONT = ("Calibri", 14)

class ReadScaleDialog(templateDialog):
	def __init__(self, partask, *args,**kwargs):
		self.partask = partask # create a local copy of parent task
		self.finishedtask = None
		tkSimpleDialog.Dialog.__init__(self, *args,**kwargs)

	def body(self, master):

		namesinscope = self.partask.list_imageout()
		tk.Label(master, text="Read Scale Name:").grid(row=0)
		tk.Label(master, text="Snapshot:").grid(row=1)
		tk.Label(master, text="Units:").grid(row=2)

		self.nameentry = tk.Entry(master)
		self.nameentry.insert(0, "ScaleReader")

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

				fc = MarkerSelectDialog([xmin,ymin], [xmax,ymax], "Select point fixed to rig", mycam, self)
				if fc.endcolor is not None:
					fixedcol = fc.endcolor
					mc = MarkerSelectDialog([xmin,ymin], [xmax,ymax], "Select moving marker", mycam, self)
					if mc.endcolor is not None:
						movingcol = mc.endcolor
						sc1 = ScaleCalibrateDialog(fixedcol,movingcol,mycam,"Move scale to minimum and enter value","0",[xmin,ymin],[xmax,ymax],self)
						if sc1.value is not None:
							self.minval = float(sc1.value)
							self.minpos = float(sc1.position[0])
							sc2 = ScaleCalibrateDialog(fixedcol,movingcol,mycam,"Move scale to maximum and enter value","20",[xmin,ymin],[xmax,ymax],self)
							if sc2.value is not None:
								maxval = float(sc2.value)
								self.deltaval = maxval - self.minval
								self.maxpos = float(sc2.position[0])
								self.deltapos = self.maxpos - self.minpos
								self.finishedtask = ImageTask(self.name, 0, snapname , IMT_readscale,[xmin,ymin],[xmax,ymax],fixedcol,movingcol,self.minpos,self.deltaval, self.minval, self.deltapos)

class ScaleCalibrateDialog(templateDialog):
	def __init__(self, fixedcol, movecol, cam, message, defaultval, point1,point2, *args,**kwargs):
		self.finishedtask = None
		self.message = message
		self.camera = cam
		self.fixedcol = fixedcol
		self.movecol = movecol
		self.defaultval = defaultval
		self.point1 = point1
		self.point2 = point2
		tkSimpleDialog.Dialog.__init__(self, *args,**kwargs)

	def body(self, master):

		tk.Label(master, text=self.message).grid(row=0)
		tk.Label(master, text="Value:").grid(row=2)

		self.valueentry = tk.Entry(master)
		self.valueentry.insert(0, self.defaultval)
		self.valueentry.grid(row=2, column=1)

		return self.valueentry # initial focus

	def apply(self):
		self.value = self.valueentry.get()
		camim = self.camera.getImage()
		camim = camim.regionSelect(self.point1[0], self.point1[1], self.point2[0], self.point2[1])
		self.sf = 300/float(camim.height)
		newim = camim.scale(self.sf)
		# Find the fixed marker
		p1 = IMT_find_col(newim, self.fixedcol)
		# Find the moving marker
		p2 = IMT_find_col(newim, self.movecol)
		# Make them relative to each other
		dx = p2[0] - p1[0]
		dy = p2[1] - p1[1]
		self.position = [dx,dy]


class MarkerSelectDialog(templateDialog):

	def __init__(self, point1, point2, message, camera, *args,**kwargs):
		self.finishedtask = None
		self.point1 = point1
		self.point2 = point2

		self.camera = camera
		self.message = message
		self.markercolor = None
		self.endcolor = None
		tkSimpleDialog.Dialog.__init__(self, *args,**kwargs)

	def body(self, master):
		contframe = tk.Frame(self)

		camframe = tk.Frame(contframe)
		timerid = self.after(100, lambda:self.pack_cam_image(camframe) )
		camframe.pack(fill = "both")

		message = tk.Label(contframe, text=self.message, font=BODY_FONT)
		message.pack(side = "bottom")

		contframe.pack(fill = "both")

	def apply(self):
		self.endcolor = self.markercolor

	def onmouse(self, event):
		self.point = [event.x, event.y]
		self.extract_marker()

	def extract_marker(self):
		camim = self.camera.getImage()
		camim = camim.regionSelect(self.point1[0], self.point1[1], self.point2[0], self.point2[1])
		sf = 300/float(camim.height)
		newim = camim.scale(sf)
		self.marker_blob(newim, self.point)

	def marker_blob(self, imin, p):
		self.markercolor = imin[p]

	def pack_cam_image(self, master):
		for s in master.pack_slaves():
			s.destroy()

		camim = self.camera.getImage()
		camim = camim.regionSelect(self.point1[0], self.point1[1], self.point2[0], self.point2[1])
		self.sf = 300/float(camim.height)
		newim = camim.scale(self.sf)

		if self.markercolor is not None:
			self.centroid = IMT_find_col(newim, self.markercolor)
			circlelayer = DrawingLayer((newim.width, newim.height))
			circlelayer.circle([self.centroid[0],self.centroid[1]], 5, color = (255,0,0))
			newim.addDrawingLayer(circlelayer)
			newim = newim.applyLayers()

		photo = ImageTk.PhotoImage(newim.getPIL()) 
		label = tk.Label(master, image=photo) 
		label.camim = photo # keep a reference! 
		label.pack() #show the image
		label.bind('<Button-1>', self.onmouse)

		timerid = master.after(100, lambda:self.pack_cam_image(master) )


if __name__ == "__main__":
	root = tk.Tk()
	MarkerSelectDialog([0,0],[400,400],"Select a colored marker fixed to the scale", Camera(1), root)
