
import Tkinter as tk
import tkSimpleDialog
from SimpleCV import Camera
from PIL import ImageTk
from LabPalEngine import *

def scan_cameras():
    existingcameras = []
    for i in range(0,10):
        try:
            camera = Camera(i)
            camera.getImage().erode()
            existingcameras.append(i)
        except:
            pass
    return existingcameras

TITLE_FONT = ("Helvetica", 22, "bold")
BODY_FONT = ("Comic Sans", 14)

class CameraMakerDialog(tkSimpleDialog.Dialog):

	def __init__(self, partask, *args,**kwargs):
		self.partask = partask # create a local copy of parent task
		self.finishedtask = None
		tkSimpleDialog.Dialog.__init__(self, *args,**kwargs)

	def body(self, master):

		tk.Label(master, text="New Snapshot Name:", font = BODY_FONT).grid(row=0)
		tk.Label(master, text="Select Camera Number:", font = BODY_FONT).grid(row=1)

		self.datavar = tk.IntVar(master)
		camlist = scan_cameras()
		if len(camlist) == 0:
			self.cancel()
		self.datavar.set(0)
		repeatlist = camlist

		self.nameentry = tk.Entry(master, font = BODY_FONT)
		self.nameentry.insert(0, "Snap")
		self.dataentry = tk.OptionMenu(master, self.datavar, *repeatlist)

		self.nameentry.grid(row=0, column=2)
		self.dataentry.grid(row=1, column=2)
		button1 = tk.Button(master, text = "Preview", font = BODY_FONT, command = self.preview)
		button1.grid(row=2, column=1)
		return self.nameentry # initial focus

	def apply(self):
		self.name = self.nameentry.get()
		self.datasource = None
		self.camnumb = self.datavar.get()
		self.finishedtask = CameraSnapshot(self.name, 0, Camera(self.camnumb))

	def preview(self):
		LiveCameraDialog(Camera(self.datavar.get()),self)

	def buttonbox(self):
		box = tk.Frame(self)
		w = tk.Button(box, text="Cancel", font = BODY_FONT, width=10, command=self.cancel)
		w.pack(side = "right", padx=5, pady=5)
		self.bind("<Escape>", self.cancel)
		q = tk.Button(box, text="Ok", font = BODY_FONT, width=10, command=self.ok)
		q.pack(side = "left", padx=5, pady=5)
		self.bind("<Return>", self.ok)
		box.pack(side = "bottom")


def pack_cam_image(master, parentdialog):
	for s in master.pack_slaves():
		s.destroy()
	camim = parentdialog.camera.getImage()
	sf = 300/float(camim.height)
	photo = ImageTk.PhotoImage(camim.scale(sf).getPIL()) 
	label = tk.Label(master, image=photo) 
	label.camim = photo # keep a reference! 
	label.pack() #show the image
	timerid = master.after(100, lambda:pack_cam_image(master, parentdialog) )

class LiveCameraDialog(tkSimpleDialog.Dialog):

	def __init__(self, camera, *args,**kwargs):
		self.camera = camera
		tkSimpleDialog.Dialog.__init__(self, *args,**kwargs)

	def body(self, master):
		contframe = tk.Frame(self)
		
		timerid = self.after(100, lambda:pack_cam_image(contframe, self) )

		contframe.pack(fill = "both")

	def buttonbox(self):
		box = tk.Frame(self)
		w = tk.Button(box, text="Cancel", font = BODY_FONT, width=10, command=self.cancel)
		w.pack(padx=5, pady=5)
		self.bind("<Escape>", self.cancel)
		box.pack()
