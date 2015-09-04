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
	btn1 = tk.Button(buttonholder, text='New Camera Snapshot', command=lambda: runCameraMaker(looptask,yesubframe))
	btn2 = tk.Button(buttonholder, text='New Image Processing Task', command=lambda: runImageTaskMaker(looptask,yesubframe))
	btn3 = tk.Button(buttonholder, text='New Loop', command=lambda: runLoopMaker(looptask,yesubframe))
	btn1.pack(side = "right")
	btn2.pack(side = "right")
	btn3.pack(side = "right")
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

def runImageTaskMaker(looptask, master):
	namesinscope = [ task.name for task in looptask.tasks ]
	if len(namesinscope) > 0:
		md = ImageTaskMakerDialog(looptask,master)
		if md.finishedtask is not None:
			looptask.tasks.append(md.finishedtask)
			repack_loop(looptask,master)

def runLoopMaker(looptask, master):
	md = LoopMakerDialog(looptask,master)
	if md.finishedtask is not None:
		looptask.tasks.append(md.finishedtask)
		repack_loop(looptask,master)

def runCameraMaker(looptask, master):
	md = CameraMakerDialog(looptask,master)
	if md.finishedtask is not None:
		looptask.tasks.append(md.finishedtask)
		repack_loop(looptask,master)

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








class StdoutRedirector(object):
    def __init__(self,text_widget):
        self.text_space = text_widget

    def write(self,string):
        self.text_space.insert('end', string)
        self.text_space.see('end')

class MenuApp(tk.Tk):

    def __init__(self, *args, **kwargs):
		tk.Tk.__init__(self, *args, **kwargs)
		# the container is where we'll stack a bunch of frames
		# on top of each other, then the one we want visible
		# will be raised above the others
		self.geometry("800x480")
		container = tk.Frame(self)
		container.pack(side="top", fill="both", expand=True)
		container.grid_rowconfigure(0, weight=1)
		container.grid_columnconfigure(0, weight=1)

		# The experiment itself belongs to this window
		myexperiment = Loop("New_Experiment",0 ,None,"minimal","repeat",1)
		myexperiment.startdirec = "./"
		myloop = Loop("Myloop",0 ,None,"minimal","repeat",100)
		myloop.add_task(CameraSnapshot("Snap1", 0, Camera(0)))
		#myloop.add_task(ImageTask("Readdigs",0,"Snap1",IMT_readdigits,[150,78],[466,251]))
		myexperiment.add_task(myloop)
		self.experiment = myexperiment

		self.frames = {}
		for F in (MenuPage, EditExperiment, ExperimentRunning):
			frame = F(container, self)
			self.frames[F] = frame
			# put all of the pages in the same location;
			# the one on the top of the stacking order
			# will be the one that is visible.
			frame.grid(row=0, column=0, sticky="nsew")

		self.show_frame(MenuPage)

    def show_frame(self, c):
        '''Show a frame for the given class'''
        frame = self.frames[c]
        frame.tkraise()
        

class MenuPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="LabPal", font=TITLE_FONT)
        label.pack(side="top", fill="x", pady=10)

        button1 = tk.Button(self, text="New Experiment",
                            command=lambda: controller.show_frame(EditExperiment),
                            font=BODY_FONT)
        button1.pack(fill="x", padx=20)

        button2 = tk.Button(self, text="Load Experiment",
                            command=lambda: controller.show_frame(EditExperiment),
                            font=BODY_FONT)
        button2.pack(fill="x", padx=20)

        button3 = tk.Button(self, text="Transfer data",
                            command=lambda: controller.show_frame(EditExperiment),
                            font=BODY_FONT)
        button3.pack(fill="x", padx=20)


class EditExperiment(tk.Frame):

	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)

		# This holds the menu section of the program
		menubar = tk.Frame(self, relief="ridge", borderwidth = 1)
		label = tk.Label(menubar, text = controller.experiment.name, font=TITLE_FONT)
		label.pack(side="right", pady=10, padx=20, fill="x")
		menubutton = tk.Button(menubar, text="Main Menu",
                            command=lambda: controller.show_frame(MenuPage),
                            font=BODY_FONT)
		menubutton.pack(side="left", fill="y")
		menubar.pack(side="top", fill="x")

		# This contains the side bar thing
		self.sidebar = tk.Frame(self, borderwidth=2, width= 200, relief="ridge")
		# Startbutton
		startbutton = tk.Button(self.sidebar, text = "START",
                            command=lambda: self.start_experiment(controller),
                            font=BODY_FONT, bg="#5DFC0A")
		startbutton.pack(side = "bottom", fill="x", expand = True)
		# Savebutton
		savebutton = tk.Button(self.sidebar, text = "SAVE",
                            command=lambda: controller.show_frame(ExperimentRunning),
                            font=BODY_FONT, bg="#0000FF")
		savebutton.pack(side = "bottom", fill ="x", expand = True)
		# Renamebutton
		renamebutton = tk.Button(self.sidebar, text = "RENAME",
                            command=lambda: controller.show_frame(ExperimentRunning),
                            font=BODY_FONT, bg="#FF0000")
		renamebutton.pack(side = "bottom", fill="x", expand = True)
		self.sidebar.pack(fill = "y", side = "right")

		# This contains the interactive section for setup of the experiment
		self.contentframe = VerticalScrolledFrame(self)
		pack_task(controller.experiment,self.contentframe.interior,None)
		self.contentframe.pack(fill = "both", pady=10, side = "left",expand=True)

	def start_experiment(self, controller):
		controller.show_frame(ExperimentRunning)
		begin_experiment(controller.experiment)


class ExperimentRunning(tk.Frame):
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)

		# This contains the menu area at the top
		menubar = tk.Frame(self, relief="ridge", borderwidth = 1)
		label = tk.Label(menubar, text=controller.experiment.name, font=TITLE_FONT)
		label.pack(pady=10, padx=20, fill="x")
		menubar.pack(side="top", fill="x")

		# This contains the side bar thing
		self.sidebar = tk.Frame(self, borderwidth=2, relief="ridge")
		# Discardbutton
		Discardbutton = tk.Button(self.sidebar, text = "DISCARD\nEXPERIMENT",
                            command=lambda: self.stop_experiment(controller),
                            font=BODY_FONT)
		Discardbutton.pack(side = "bottom", fill="x", expand = True)
		# Stopbutton
		stopbutton = tk.Button(self.sidebar, text = "STOP\nEXPERIMENT",
                            command=lambda: self.stop_experiment(controller),
                            font=BODY_FONT, bg="#FF0000")
		stopbutton.pack(side = "bottom", fill ="x", expand = True)
		self.sidebar.pack(fill = "both", side = "right")

		# This contains the piped stdout
		self.contentframe = tk.Frame(self)
		textscroller = tk.Scrollbar(self.contentframe)
		self.stdtext = tk.Text(self.contentframe, font = BODY_FONT)
		self.stdtext.pack(side="left", fill = "both")
		textscroller.pack(side="left", fill="y")
		textscroller.config(command=self.stdtext.yview)
		self.stdtext.config(yscrollcommand=textscroller.set)

		self.contentframe.pack(fill = "both", side = "left", expand=True)
		sys.stdout = StdoutRedirector(self.stdtext)

	def stop_experiment(self, controller):
		end_experiment(controller.experiment)
		controller.show_frame(EditExperiment)
		self.stdtext.delete(1.0, "end")


if __name__ == "__main__":
	app = MenuApp()
	app.mainloop()