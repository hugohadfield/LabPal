
import Tkinter as tk
from templateDialog import *
from LabPalEngine import *

TITLE_FONT = ("Calibri", 22, "bold")
BODY_FONT = ("Calibri", 14)

class UserPromptDialog(templateDialog):
	def __init__(self, partask, *args,**kwargs):
		self.partask = partask # create a local copy of parent task
		self.finishedtask = None
		tkSimpleDialog.Dialog.__init__(self, *args,**kwargs)

	def body(self, master):

		namesinscope = self.partask.list_imageout()
		tk.Label(master, text="User Prompt Name:").grid(row=0)
		tk.Label(master, text="Message:").grid(row=1)
		tk.Label(master, text="Duration:").grid(row=2)

		self.nameentry = tk.Entry(master)
		self.nameentry.insert(0, "User_Prompt")

		self.messageentry = tk.Entry(master)
		self.messageentry.insert(0, "")
		
		self.durationentry = tk.Entry(master)
		self.durationentry.insert(0, "30")

		self.nameentry.grid(row=0, column=1)
		self.messageentry.grid(row=1, column=1)
		self.durationentry.grid(row=2, column=1)
		return self.nameentry # initial focus


	def apply(self):
		self.name = self.nameentry.get()
		self.message = self.messageentry.get()
		self.duration = int(self.durationentry.get())
		self.finishedtask = UserPromptTask(self.name, 0, None, self.message, self.duration)