
import Tkinter as tk
import tkSimpleDialog
from LabPalEngine import *
import sys

from CameraGUI import *
from GroupGUI import *
from ScaleGUI import *
from ScreenGUI import *
from UserPromptGUI import *

TITLE_FONT = ("Calibri", 22, "bold")
BODY_FONT = ("Calibri", 14)

class VerticalScrolledFrame(tk.Frame):
    """A pure Tkinter scrollable frame that actually works!
    * Use the 'interior' attribute to place widgets inside the scrollable frame
    * Construct and pack/place/grid normally
    * This frame only allows vertical scrolling

    """
    def __init__(self, parent, *args, **kw):
        tk.Frame.__init__(self, parent, *args, **kw)            

        # create a canvas object and a vertical scrollbar for scrolling it
        vscrollbar = tk.Scrollbar(self, orient="vertical")
        vscrollbar.pack(fill="y", side="right", expand="False")
        canvas = tk.Canvas(self, bd=0, highlightthickness=0,
                        yscrollcommand=vscrollbar.set)
        canvas.pack(side="left", fill="both", expand="True")
        vscrollbar.config(command=canvas.yview)

        # reset the view
        canvas.xview_moveto(0)
        canvas.yview_moveto(0)

        # create a frame inside the canvas which will be scrolled with it
        self.interior = interior = tk.Frame(canvas)
        interior_id = canvas.create_window(0, 0, window=interior,
                                           anchor="nw")

        # track changes to the canvas and frame width and sync them,
        # also updating the scrollbar
        def _configure_interior(event):
            # update the scrollbars to match the size of the inner frame
            size = (interior.winfo_reqwidth(), interior.winfo_reqheight())
            canvas.config(scrollregion="0 0 %s %s" % size)
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # update the canvas's width to fit the inner frame
                canvas.config(width=interior.winfo_reqwidth())
        interior.bind('<Configure>', _configure_interior)

        def _configure_canvas(event):
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # update the inner frame's width to fill the canvas
                canvas.itemconfigure(interior_id, width=canvas.winfo_width())
        canvas.bind('<Configure>', _configure_canvas)


class RemovableElement(tk.Frame):
    def __init__(self, master, assoctask, partask, **options):
        tk.Frame.__init__(self, master, **options)
        mbar =  tk.Frame(self)
        lbl = tk.Label(mbar, text=assoctask.name, font=BODY_FONT)
        if partask is not None:
        	btn = tk.Button(mbar, text='x', command=lambda: self.remove(assoctask,partask), font=BODY_FONT)
        	btn.pack(side = "right")
        lbl.pack(side = "left")
        mbar.pack(side = "top", fill="x")
        self.subframe = tk.Frame(self)
    def remove(self,assoctask,partask):
		partask.delete_task(assoctask)
		self.destroy()


def pack_loop_buttons(looptask,yesubframe):
	buttonholder = tk.Frame(yesubframe)
	btn1 = tk.Button(buttonholder, text='New...', font=BODY_FONT, command=lambda: runNewTaskMaker(looptask,yesubframe))
	btn1.pack(side = "right")
	buttonholder.pack(side = "bottom")

def pack_task(mytask, parframe, partask):
	e = RemovableElement(parframe, mytask, partask, relief="ridge", borderwidth = 1)
	try:
		if len(mytask.tasks) > 0:
			for task in mytask.tasks:
				pack_task(task, e.subframe, mytask)
		pack_loop_buttons(mytask,e.subframe)
	except:
		pass
	e.subframe.pack(side = "bottom", fill = 'x',  padx=10)
	e.pack(side = "top", fill="x",  padx=10)

def repack_loop(looptask,master):
	for s in master.pack_slaves():
		s.destroy()
	for task in looptask.tasks:
		pack_task(task, master, looptask)
	pack_loop_buttons(looptask,master)









def lol():
	pass

class NewTaskDialog(tkSimpleDialog.Dialog):

	def __init__(self, partask, *args,**kwargs):
		self.partask = partask # create a local copy of parent task
		self.finishedtask = None
		tkSimpleDialog.Dialog.__init__(self, *args,**kwargs)

	def body(self, master):
		contframe = tk.Frame(self)
		vsf = VerticalScrolledFrame(contframe)
		buttons = [ tk.Button(vsf.interior, text='Group', font=BODY_FONT, command=self.MakeLoop),
					tk.Button(vsf.interior, text='Camera Snapshot', font=BODY_FONT, command=self.MakeCamera),
					tk.Button(vsf.interior, text='User Prompt', font=BODY_FONT, command=self.MakeUserPrompt),
					tk.Button(vsf.interior, text='Read Screen', font=BODY_FONT, command=self.MakeScreenReader),
					tk.Button(vsf.interior, text='Read Scale', font=BODY_FONT, command=self.MakeScaleReader),
					tk.Button(vsf.interior, text='Marker Tracker', font=BODY_FONT, command=self.MakeMarkerTracker),
					tk.Button(vsf.interior, text='Read Arduino Temperature', font=BODY_FONT, command=self.MakeArduinoReader),
					tk.Button(vsf.interior, text='User Input', font=BODY_FONT, command=self.MakeUserInput) ]
		for but in buttons:
			but.pack(fill = "x", padx = 10, pady = 2)
		vsf.pack(fill = "both")
		contframe.pack(fill = "both")

	def buttonbox(self):
		box = tk.Frame(self)
		w = tk.Button(box, text="Cancel", font = BODY_FONT, width=10, command=self.cancel)
		w.pack(padx=5, pady=5)
		self.bind("<Escape>", self.cancel)
		box.pack()

	def MakeCamera(self):
		self.parent.focus_set()
		md = CameraMakerDialog(self.partask,self.master)
		self.finishedtask = md.finishedtask
		self.cancel()

	def MakeImage(self):
		self.parent.focus_set()
		namesinscope = [ task.name for task in self.partask.tasks ]
		if len(namesinscope) > 0:
			md = ImageMakerDialog(self.partask,self.master)
			self.finishedtask = md.finishedtask 
		self.cancel()

	def MakeLoop(self):
		self.parent.focus_set()
		md = LoopMakerDialog(self.partask,self.master)
		self.finishedtask = md.finishedtask
		self.cancel()

	def MakeMarkerTracker(self):
		self.parent.focus_set()
		md = LoopMakerDialog(self.partask,self.master)
		self.finishedtask = md.finishedtask
		self.cancel()

	def MakeScreenReader(self):
		self.parent.focus_set()
		md = ReadScreenDialog(self.partask,self.master)
		self.finishedtask = md.finishedtask
		self.cancel()

	def MakeScaleReader(self):
		self.parent.focus_set()
		md = ReadScaleDialog(self.partask,self.master)
		self.finishedtask = md.finishedtask
		self.cancel()

	def MakeArduinoReader(self):
		self.parent.focus_set()
		md = LoopMakerDialog(self.partask,self.master)
		self.finishedtask = md.finishedtask
		self.cancel()

	def MakeUserPrompt(self):
		self.parent.focus_set()
		md = UserPromptDialog(self.partask,self.master)
		self.finishedtask = md.finishedtask
		self.cancel()

	def MakeUserInput(self):
		self.parent.focus_set()
		md = LoopMakerDialog(self.partask,self.master)
		self.finishedtask = md.finishedtask
		self.cancel()


def runNewTaskMaker(looptask, master):
	md = NewTaskDialog(looptask,master)
	if md.finishedtask is not None:
		looptask.tasks.append(md.finishedtask)
		repack_loop(looptask,master)