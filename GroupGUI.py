
import Tkinter as tk
from templateDialog import *
from LabPalEngine import *

TITLE_FONT = ("Calibri", 22, "bold")
BODY_FONT = ("Calibri", 14)

class LoopRepeatDialog(templateDialog):
	def __init__(self, *args,**kwargs):
		self.finishedtask = None
		tkSimpleDialog.Dialog.__init__(self, *args,**kwargs)

	def body(self, master):

		tk.Label(master, text="Number of repeats:", font=BODY_FONT).grid(row=0)
		tk.Label(master, text="Repeat frequency (Hz):", font=BODY_FONT).grid(row=1)

		self.numberentry = tk.Entry(master)
		self.numberentry.insert(0, "5")
		self.frequencyentry = tk.Entry(master)
		self.frequencyentry.insert(0, "10")

		self.numberentry.grid(row=0, column=1)
		self.frequencyentry.grid(row=1, column=1)
		return self.numberentry # initial focus

	def apply(self):
		self.frequency = float(self.frequencyentry.get())
		looptime = 1/self.frequency
		self.repeats = int(self.numberentry.get())
		self.finishedtask=Loop("tname", 0, None, looptime ,"repeat", self.repeats)


class LoopDurationDialog(templateDialog):
	def __init__(self, *args,**kwargs):
		self.finishedtask = None
		tkSimpleDialog.Dialog.__init__(self, *args,**kwargs)

	def body(self, master):

		gridframe = tk.Frame(master)

		tk.Label(gridframe, text="Set Duration:", font=BODY_FONT).grid(row=0)

		self.Days = tk.Entry(gridframe)
		self.Days.insert(0, "0")
		self.Days.grid(row=1)

		self.Hours = tk.Entry(gridframe)
		self.Hours.insert(0, "0")
		self.Hours.grid(row=1, column=1)

		self.Minutes = tk.Entry(gridframe)
		self.Minutes.insert(0, "0")
		self.Minutes.grid(row=1, column=2)

		self.Seconds = tk.Entry(gridframe)
		self.Seconds.insert(0, "10")
		self.Seconds.grid(row=1, column=3)

		tk.Label(gridframe, text="Days:", font=BODY_FONT).grid(row=2)
		tk.Label(gridframe, text="Hours:", font=BODY_FONT).grid(row=2, column=1)
		tk.Label(gridframe, text="Minutes:", font=BODY_FONT).grid(row=2, column=2)
		tk.Label(gridframe, text="Seconds:", font=BODY_FONT).grid(row=2, column=3)


		tk.Label(gridframe, text="Repeat frequency (Hz):", font=BODY_FONT).grid(row=3)
		self.frequencyentry = tk.Entry(gridframe)
		self.frequencyentry.insert(0, "10")
		self.frequencyentry.grid(row=3, column=1)

		gridframe.pack()

		return self.Seconds # initial focus

	def apply(self):
		self.frequency = float(self.frequencyentry.get())
		looptime = 1/self.frequency
		self.timeout = int(self.Seconds.get()) + 60*(int(self.Minutes.get()) + 60*(int(self.Hours.get()) + 24*int(self.Days.get())))
		self.finishedtask=Loop("tname", 0, None, looptime ,"timeout", self.timeout)



class LoopMakerDialog(templateDialog):

	def __init__(self, partask, *args,**kwargs):
		self.partask = partask # create a local copy of parent task
		self.finishedtask = None
		tkSimpleDialog.Dialog.__init__(self, *args,**kwargs)

	def body(self, master):

		tk.Label(master, text="Group Name:", font=BODY_FONT).grid(row=0)
		tk.Label(master, text="Repeats:", font=BODY_FONT).grid(row=1)

		self.datavar = tk.StringVar(master)
		self.datavar.set("None")
		repeatlist = ["None","N Times","Set Duration","Continuous"]

		self.nameentry = tk.Entry(master)
		self.nameentry.insert(0, "Group")
		self.dataentry = tk.OptionMenu(master, self.datavar, *repeatlist)

		self.nameentry.grid(row=0, column=1)
		self.dataentry.grid(row=1, column=1)
		return self.nameentry # initial focus

	def apply(self):
		self.name = self.nameentry.get()
		self.datasource = None
		self.repeats = self.datavar.get()
		if self.repeats == "Continuous":
			pass
		elif self.repeats == "N Times":
			md = LoopRepeatDialog(self)
			if md.finishedtask is not None:
				self.finishedtask = md.finishedtask
				self.finishedtask.name = self.name
			self.cancel()
		elif self.repeats == "Set Duration":
			md = LoopDurationDialog(self)
			if md.finishedtask is not None:
				self.finishedtask = md.finishedtask
				self.finishedtask.name = self.name
			self.cancel()
		elif self.repeats == "None":
			self.finishedtask = Loop(self.name,0, None, "minimal", "repeat", 0)
			self.cancel()
