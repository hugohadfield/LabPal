from subprocess import Popen, PIPE
import os

def imagefiletostring(imagefile, *args):
	argstring = " -t20 -d-1 -i3 remove_isolated " + imagefile
	comstring = "ssocr.exe" + argstring
	p = Popen(comstring, shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE)
	output, err = p.communicate(b"input data that is passed to subprocess' stdin")
	rc = p.returncode
	return output

def imagefiletofloat(imagefile, *args):
	strout = imagefiletostring(imagefile, args)
	try:
		nout = float(strout)
	except:
		print "Could not convert: " + strout + " to float"
		raise
	return nout

if __name__ == "__main__":
	print imagefiletofloat("temp.jpg")