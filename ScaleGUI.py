
import Tkinter as tk
import tkSimpleDialog

TITLE_FONT = ("Helvetica", 22, "bold")
BODY_FONT = ("Comic Sans", 14)

class ImageTaskMakerDialog(tkSimpleDialog.Dialog):

	def __init__(self, partask, *args,**kwargs):
		self.partask = partask # create a local copy of parent task
		self.finishedtask = None
		tkSimpleDialog.Dialog.__init__(self, *args,**kwargs)

	def body(self, master):

		namesinscope = self.partask.list_imageout()
		tk.Label(master, text="New task name:").grid(row=0)
		tk.Label(master, text="New task function:").grid(row=1)
		tk.Label(master, text="Get data from:").grid(row=2)

		self.datavar = tk.StringVar(master)
		self.datavar.set(namesinscope[0])

		self.nameentry = tk.Entry(master)
		self.nameentry.set("ImageTask")
		self.dataentry = tk.OptionMenu(master, self.datavar, *namesinscope)

		self.nameentry.grid(row=0, column=1)
		self.dataentry.grid(row=2, column=1)
		return self.nameentry # initial focus

	def apply(self):
		self.name = self.nameentry.get()
		self.datasource = self.datavar.get()
		self.finishedtask = ImageTask(self.name, 0, self.datasource, IMT_sumbox, [0,0],[100,100])



