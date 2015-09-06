
import Tkinter as tk
import tkSimpleDialog

BODY_FONT = ("Calibri", 14)

class templateDialog(tkSimpleDialog.Dialog):

	def buttonbox(self):
		box = tk.Frame(self)
		w = tk.Button(box, text="Cancel", font = BODY_FONT, width=10, command=self.cancel)
		w.pack(side = "right", padx=5, pady=5)
		self.bind("<Escape>", self.cancel)
		q = tk.Button(box, text="OK", font = BODY_FONT, width=10, command=self.ok)
		q.pack(side = "left", padx=5, pady=5)
		self.bind("<Return>", self.ok)
		box.pack(side = "bottom")