
		# This creates a cartesian distance map from the point of the click
		xvals = np.arange(0,imin.width)
		xsqr = np.square( (xvals - p[0]) )
		yvals = np.arange(0,imin.height)
		ysqr = np.square( (yvals - p[1]) )
		fullxsqr = np.transpose( np.tile( xsqr, (imin.height,1) ) )
		fullysqr = np.tile( ysqr, (imin.width,1) )  
		dist = npboost( np.sqrt(fullysqr + fullxsqr) )

		# This is the color distance from the reference point
		coldist = imin.colorDistance( imin[p] )

		lolout = Image( npboost(   dist + np.squeeze(np.dsplit( coldist.getNumpy(), 3)[0] )  ) )
		blobs = lolout.stretch(0,20).invert().findBlobs()
		lolout.stretch(0,20).invert().show()

		