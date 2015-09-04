
import Tkinter as tk
import tkSimpleDialog
from TaskMaster import *
from SimpleCV import Camera
import sys

TITLE_FONT = ("Helvetica", 22, "bold")
BODY_FONT = ("Comic Sans", 14)

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
	btn1 = tk.Button(buttonholder, text='New...', command=lambda: runNewTaskMaker(looptask,yesubframe))
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










class LoopMakerDialog(tkSimpleDialog.Dialog):

	def __init__(self, partask, *args,**kwargs):
		self.partask = partask # create a local copy of parent task
		self.finishedtask = None
		tkSimpleDialog.Dialog.__init__(self, *args,**kwargs)

	def body(self, master):

		tk.Label(master, text="New Loop Name:").grid(row=0)
		tk.Label(master, text="Repeats:").grid(row=1)

		self.datavar = tk.StringVar(master)
		self.datavar.set("Manually end loop")
		repeatlist = ["1","10","100","1000","10000","100000"]

		self.nameentry = tk.Entry(master)
		self.dataentry = tk.OptionMenu(master, self.datavar, *repeatlist)

		self.nameentry.grid(row=0, column=1)
		self.dataentry.grid(row=1, column=1)
		return self.nameentry # initial focus

	def apply(self):
		self.name = self.nameentry.get()
		self.datasource = None
		self.repeats = self.datavar.get()
		if self.repeats == "Manually end loop":
			self.finishedtask = Loop(self.name, 0, endcondition = "manual")
		else: 
			self.finishedtask = Loop(self.name, 0, None, "minimal", "repeat", int(self.repeats))



class CameraMakerDialog(tkSimpleDialog.Dialog):

	def __init__(self, partask, *args,**kwargs):
		self.partask = partask # create a local copy of parent task
		self.finishedtask = None
		tkSimpleDialog.Dialog.__init__(self, *args,**kwargs)

	def body(self, master):

		tk.Label(master, text="New Snapshot Name:").grid(row=0)
		tk.Label(master, text="Select Camera Number:").grid(row=1)

		self.datavar = tk.IntVar(master)
		camlist = scan_cameras()
		if len(camlist) == 0:
			pass # TODO something sensible
		self.datavar.set(0)
		repeatlist = camlist

		self.nameentry = tk.Entry(master)
		self.dataentry = tk.OptionMenu(master, self.datavar, *repeatlist)

		self.nameentry.grid(row=0, column=1)
		self.dataentry.grid(row=1, column=1)
		return self.nameentry # initial focus

	def apply(self):
		self.name = self.nameentry.get()
		self.datasource = None
		self.camnumb = self.datavar.get()
		self.finishedtask = CameraSnapshot(self.name, 0, Camera(self.camnumb))



class ImageTaskMakerDialog(tkSimpleDialog.Dialog):

	def __init__(self, partask, *args,**kwargs):
		self.partask = partask # create a local copy of parent task
		self.finishedtask = None
		tkSimpleDialog.Dialog.__init__(self, *args,**kwargs)

	def body(self, master):

		namesinscope = [ task.name for task in self.partask.tasks ]
		tk.Label(master, text="New task name:").grid(row=0)
		tk.Label(master, text="New task function:").grid(row=1)
		tk.Label(master, text="Get data from:").grid(row=2)

		self.datavar = tk.StringVar(master)
		self.datavar.set(namesinscope[0])

		self.nameentry = tk.Entry(master)
		self.dataentry = tk.OptionMenu(master, self.datavar, *namesinscope)

		self.nameentry.grid(row=0, column=1)
		self.dataentry.grid(row=2, column=1)
		return self.nameentry # initial focus

	def apply(self):
		self.name = self.nameentry.get()
		self.datasource = self.datavar.get()
		self.finishedtask = ImageTask(self.name, 0, self.datasource, IMT_sumbox, [0,0],[100,100])

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
					tk.Button(vsf.interior, text='Marker Tracker', font=BODY_FONT, command=lol),
					tk.Button(vsf.interior, text='Read Screen', font=BODY_FONT, command=lol),
					tk.Button(vsf.interior, text='Read Scale', font=BODY_FONT, command=lol),
					tk.Button(vsf.interior, text='Read Arduino Temperature', font=BODY_FONT, command=lol),
					tk.Button(vsf.interior, text='User Prompt', font=BODY_FONT, command=lol),
					tk.Button(vsf.interior, text='User Input', font=BODY_FONT, command=lol) ]
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


def runNewTaskMaker(looptask, master):
	md = NewTaskDialog(looptask,master)
	if md.finishedtask is not None:
		looptask.tasks.append(md.finishedtask)
		repack_loop(looptask,master)



# def new_task(looptask,yesubframe):
	# top = tkSimpleDialog()
	# top.geometry("%dx%d%+d%+d" % (600, 200, 250, 125))
	# vsf = VerticalScrolledFrame()
	# buttons = [ tk.Button(vsf, text='Group',  command=lambda: pass),
				# tk.Button(vsf, text='Camera Snapshot', command=lambda: ),
				# tk.Button(vsf, text='Marker Tracker', command=lambda: ),
				# tk.Button(vsf, text='Read Screen', command=lambda: ),
				# tk.Button(vsf, text='Read Scale', command=lambda: ),
				# tk.Button(vsf, text='Read Arduino Temperature', command=lambda: ),
				# tk.Button(vsf, text='User Prompt', command=lambda: ),
				# tk.Button(vsf, text='User Input', command=lambda: ) ]

if __name__ == "__main__":
	t1 = Loop("t1", 0)
	root = tk.Tk()
	runNewTaskMaker(t1, root)