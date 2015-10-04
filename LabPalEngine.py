
# coding: utf-8

from PIL import Image as PILimage
from SimpleCV import *
from pyssocr import *

import numpy as np
import time
import datetime
from collections import defaultdict
import threading
import sys
import os

LOOPBREAK = False
breaklock = threading.Lock()

def begin_experiment(experiment):
    experiment.workerthread = threading.Thread(target=experiment.run, args=())
    experiment.workerthread.start()

def end_experiment(experiment):
    breaklock.acquire()
    global LOOPBREAK
    LOOPBREAK = True
    breaklock.release()
    experiment.workerthread.join()

def m_open(imin,iterations):
    myim = imin.erode(iterations)
    return myim.dilate(iterations)

def m_close(imin,iterations):
    myim = imin.dilate(iterations)
    return myim.erode(iterations)

def simplecv2PIL(imin):
    imnp = imin.rotate90().getNumpy()
    im = PILimage.fromarray(np.uint8(imnp))
    return im

def simplecvboost(imin):
    imnp = imin.getNumpy()
    im = Image(np.uint8(npboost(imnp)))
    return im
    
def checkforexit():
    breaklock.acquire()
    breakbool = LOOPBREAK
    breaklock.release()
    return breakbool
    
def npboost(imin):
    baseline = (imin.real.astype(float) - np.min(imin))
    boosted = 255 * baseline/np.max(baseline)
    return boosted

def run_for(f, duration, *args):
    t1 = time.time()
    if len(args) > 0:
        fout = f(*args)
    else:
        fout = f()
    tend = time.time()
    delta_t = duration - (tend - t1)
    if  delta_t < 0:
        delta_t = 0
    time.sleep(delta_t)
    return [fout,tend]

def scan_cameras():
    existingcameras = []
    for i in range(0,10):
        try:
            camera = Camera(i)
            camera.getImage().erode()
            existingcameras.append(i)
        except:
            pass
    return existingcameras

def IMT_save(imin, *args):
    imin.save(args[0]) # args[0] is the filename
    
def IMT_sumbox(imin, *args):
    imtemp = imin.getGrayscaleMatrix()
    imslice = imtemp[args[0][0]:args[1][0],args[0][1]:args[1][1]] #args consists of 2 points specifying top left and bottom right
    outsum = np.sum(imslice)
    return outsum

def IMT_readdigits(imin, *args):
    xmin = args[0][0]
    xmax = args[1][0]
    ymin = args[0][1]
    ymax = args[1][1]
    imslice = imin.regionSelect(xmin, ymin, xmax, ymax)
    sf = 150/float(imslice.height)
    imslice = simplecvboost(imslice.scale(sf).grayscale())
    imslice.save("temp.jpg")
    digits = imagefiletostring("temp.jpg")
    return digits

def IMT_smooth(imin, *args):
    return imin.smooth( aperature = args[0])

class Task:
    def __init__(self, name, starttime, provider_task):
        self.name = name
        self.starttime = starttime
        self.provider_task = provider_task

class CameraSnapshot(Task):
    def __init__(self, name, starttime, camera):
        provider_task = None
        Task.__init__(self, name, starttime, provider_task)
        self.camera = camera
        self.duration = 0.05
        self.endtime = self,starttime + self.duration
    def run(self):
        return run_for(self.camera.getImage, self.duration)
    
class ImageTask(Task):
    def __init__(self, name, starttime, provider_task , func, *args):
        Task.__init__(self, name, starttime, provider_task)
        self.func = func
        self.duration = 0.005
        self.args = args
    def run(self, image):
        return run_for(self.func, self.duration, image, *self.args)
    
class Loop(Task):
    def __init__(self, name, starttime, provider_task = None, looptime = "minimal", endcondition = "manual", *args):
        Task.__init__(self, name, starttime, provider_task)
        self.endcondition = endcondition
        self.looptime = looptime
        self.tasks = []
        self.data = defaultdict(list)
        if endcondition == "repeat":
            self.repeats = args[0]
        elif endcondition == "timeout":
            self.timeout = args[0]
    def add_task(self, task):
        self.tasks.append(task)
    def delete_task(self, task):
        if task in self.tasks:
            self.tasks.remove(task)
    def calc_task_duration(self):
        dsum = 0
        for task in self.tasks:
            dsum = dsum + task.duration
        return dsum
    def get_duration(self):
        if self.endcondition == "repeat":
            return self.repeats * self.calc_task_duration()
        elif self.endcondition == "timeout":
            return self.timeout
    duration = property(get_duration)

    def list_numeric(self):
        outputnames = []
        for task in self.tasks:
            if isinstance(task,ImageTask):
                outputnames.append(task.name)
        return outputnames

    def list_imageout(self):
        outputnames = []
        for task in self.tasks:
            if isinstance(task,CameraSnapshot):
                outputnames.append(task.name)
        return outputnames

    def list_text(self):
        outputnames = []
        for task in self.tasks:
            if isinstance(task,ImageTask):
                outputnames.append(task.name)
        return outputnames

    def gen_files(self):
        ts = time.time()
        st = datetime.datetime.fromtimestamp(ts).strftime('_%Y_%m_%d_%H_%M_%S')
        self.datadirec = self.startdirec + self.name + st + "/"
        for task in self.tasks:
            task.startdirec = self.datadirec
        os.mkdir(self.datadirec)
        self.imagedir = self.datadirec + self.name + "_images/"
        os.mkdir(self.imagedir)
        self.fileobj = open(self.datadirec + self.name + ".txt", 'w+')
        namelist = self.list_numeric() + self.list_text()
        self.fileobj.write( ",".join(namelist) )
        self.fileobj.write('\n')

    def savedatum(self,name,datum):
        if name in self.list_numeric():
            self.fileobj.write( name )
            self.fileobj.write(',')
            self.fileobj.write( str(datum[0]) )
            self.fileobj.write(',')
            self.fileobj.write( str(datum[1]) )
            self.fileobj.write('\n')
        else:
            if name in self.list_imageout():
                st = datetime.datetime.fromtimestamp(datum[1]).strftime('_%Y_%m_%d_%H_%M_%S')
                fname = self.imagedir + self.name + st
                if not os.path.isfile(fname+".jpg"):
                    datum[0].save(fname+".jpg")
                    return
                n = 2
                while 1:
                    if os.path.isfile(self.imagedir + self.name + st + '_' + str(n)+".jpg"):
                        n = n+1
                    else:
                        break
                datum[0].save(self.imagedir + self.name + st + '_' + str(n)+".jpg")

    def execloop(self):
        if checkforexit():
            return False
        for task in self.tasks:
            tget = task.provider_task
            if tget is not None:
                datum = task.run( self.data[tget][0] )
            else:
                datum = task.run()
            self.data[task.name] = datum
            self.savedatum(task.name,datum)
        return True

    def run(self):

        print "Now running: " + self.name

        self.gen_files()

        if self.looptime == "minimal" and self.endcondition == "manual":
            while 1:
                if not self.execloop():
                    break
        elif self.looptime == "minimal" and self.endcondition == "repeat":
            for i in range(0,self.repeats+1):
                if not self.execloop():
                    break
        elif self.looptime == "minimal" and self.endcondition == "timeout":
            t1 = time.time()
            while time.time() - t1 < self.timeout:
                if not self.execloop():
                    break

        elif self.looptime != "minimal" and self.endcondition == "repeat":
            for i in range(0,self.repeats+1):
                retdat = run_for(self.execloop, self.looptime)
                if not retdat[0]:
                    break
        elif self.looptime != "minimal" and self.endcondition == "manual":
            while 1:
                retdat = run_for(self.execloop, self.looptime)
                if not retdat[0]:
                    break
        elif self.looptime != "minimal" and self.endcondition == "timeout":
            t1 = time.time()
            while time.time() - t1 < self.timeout:
                retdat = run_for(self.execloop, self.looptime)
                if not retdat[0]:
                    break

        print "Exiting " + self.name
        self.fileobj.close()
        return
