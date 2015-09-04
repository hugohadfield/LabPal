
import Tkinter as tk

TITLE_FONT = ("Helvetica", 18, "bold")


class MenuApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.geometry("800x480")
        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (PageBrowser, PageSetup, PageRunning):
            frame = F(container, self)
            self.frames[F] = frame
            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(PageBrowser)

    def show_frame(self, c):
        '''Show a frame for the given class'''
        frame = self.frames[c]
        frame.tkraise()
        

class PageBrowser(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Experiment Browser", font=TITLE_FONT)
        label.pack(side="top", fill="x", pady=10)

        button = tk.Button(self, text="Edit Experiment",
                            command=lambda: controller.show_frame(PageSetup))
        button.pack()


class PageSetup(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Edit Experiment", font=TITLE_FONT)
        label.pack(side="top", fill="x", pady=10)
        
        # This holds the menu section of the program
        menubar = tk.Frame(self, relief="ridge", borderwidth = 1)
        button1 = tk.Button(menubar, text="Experiment Browser",
                           command=lambda: controller.show_frame(PageBrowser))
        button2 = tk.Button(menubar, text="Run Experiment",
                           command=lambda: controller.show_frame(PageRunning))
        button1.pack(side = "left", padx=10, pady=3)
        button2.pack(side = "right", padx=10, pady=3)
        menubar.pack(side="top", fill="x")
        
        # This contains the interactive section for setup of the experiment
        self.contentframe = tk.Frame(self)
        
        self.taskframe = tk.Frame(self.contentframe)
        self.additionsframe = tk.Frame(self.contentframe)
        cambutton = tk.Button(self.additionsframe,text="Add Camera Snapshot",command=self.addCamSnap)
        improcbutton = tk.Button(self.additionsframe,text="Add Image Processing Task",command=self.addImgProc)
        loopbutton = tk.Button(self.additionsframe,text="Add Loop",command=self.addLoop)
        loopbutton.pack(side = "top", fill="x")
        cambutton.pack(side = "top", fill="x")
        improcbutton.pack(side = "top", fill="x")
        
        self.taskframe.pack(side = "left", fill = "both", padx=10, expand = 380)
        self.additionsframe.pack(side = "right",  fill = "both", padx=10, expand = 380)
 
        self.contentframe.pack(fill = "x", pady=10)

    # These add elements to the experiment
    def addLoop(self):
        e = RemovableElement(self.taskframe,'Loop', relief="raised", borderwidth = 1)
        e.pack(side = "top", fill="x")
    
    def addCamSnap(self):
        e = RemovableElement(self.taskframe,'Camera Snapshot', relief="raised", borderwidth = 1)
        e.pack(side = "top", fill="x")

    def addImgProc(self):
        e = RemovableElement(self.taskframe,'Image Proccessing', relief="raised", borderwidth= 1)
        e.pack(side = "top", fill="x")


class PageRunning(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Experiment in progress", font=TITLE_FONT)
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="Halt Experiment",
                           command=lambda: controller.show_frame(PageSetup))
        button.pack()


if __name__ == "__main__":
    app = MenuApp()
    app.mainloop()

