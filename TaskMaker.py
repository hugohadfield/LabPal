import Tkinter as tk
from TaskMaster import *
from SimpleCV import Camera
import sys
from GUIelements import *

TITLE_FONT = ("Helvetica", 22, "bold")
BODY_FONT = ("Comic Sans", 14)


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