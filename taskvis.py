
import Tkinter as tk
from TaskMaker import *

class RemovableElement(tk.Frame):
    def __init__(self, master, assoctask, partask, **options):
        tk.Frame.__init__(self, master, **options)
        mbar =  tk.Frame(self)
        lbl = tk.Label(mbar, text=assoctask.name)
        if partask is not None:
        	btn = tk.Button(mbar, text='Remove Task', command=lambda: self.remove(assoctask,partask))
        	btn.pack(side = "right")
        lbl.pack(side = "left")
        mbar.pack(side = "top", fill="x")
        self.subframe = tk.Frame(self)
    def remove(self,assoctask,partask):
		partask.delete_task(assoctask)
		self.destroy()

def deprint():
	print "hello"

def pack_task(mytask, parframe, partask):
	e = RemovableElement(parframe, mytask, partask, relief="raised", borderwidth = 1)
	try:
		if len(mytask.tasks) > 0:
			for task in mytask.tasks:
				pack_task(task, e.subframe, mytask)
		print "adding button"
		btn = tk.Button(e.subframe, text='Add new task', command=lambda: runTaskMaker(mytask,e))
		btn.pack(side = "bottom")
	except:
		print "fail"
		pass
	e.subframe.pack(side = "bottom", fill = 'x',  padx=30)
	e.pack(side = "top", fill="x",  padx=30)