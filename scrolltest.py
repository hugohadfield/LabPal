from Tkinter import *

def data():
    for i in range(50):
       Label(self.contentframe,text=i).grid(row=i,column=0)
       Label(self.contentframe,text="my text"+str(i)).grid(row=i,column=1)
       Label(self.contentframe,text="..........").grid(row=i,column=2)

def myfunction(event):
    canvas.configure(scrollregion=canvas.bbox("all"),width=200,height=200)

root=Tk()
sizex = 800
sizey = 600
posx  = 100
posy  = 100
root.wm_geometry("%dx%d+%d+%d" % (sizex, sizey, posx, posy))

myself.contentframe=tk.Frame(root,relief=GROOVE,width=50,height=100,bd=1)
myself.contentframe.place(x=10,y=10)

canvas=Canvas(myself.contentframe)
self.contentframe=tk.Frame(canvas)
myscrollbar=Scrollbar(myself.contentframe,orient="vertical",command=canvas.yview)
canvas.configure(yscrollcommand=myscrollbar.set)
myscrollbar.pack(side="right",fill="y")
canvas.pack(side="left")
canvas.create_window((0,0),window=self.contentframe,anchor='nw')
self.contentframe.bind("<Configure>",myfunction)

root.mainloop()