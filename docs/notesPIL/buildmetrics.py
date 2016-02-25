"""
buildmetrics.py

This little program builds the metrics.dat file needed to properly
measure PIL fonts.
"""

from piddlePIL import *
from piddlePIL import _fontprefix, _pilFont

# fonts we're going to support
fonts = ['courier', 'helvetica', 'symbol', 'times']

# sizes we're going to support
sizes = [8, 10, 12, 14, 18, 24]

# global scratch canvas
canvas = PILCanvas( size=(200,100) )
canvas.defaultLineColor = white

# global things we're measuring
ascents = {}
descents = {}
widths = {}

def reset():
	canvas.clear()
	canvas.drawRect( 0,0,200,100, edgeColor=black, fillColor=black )
	
def fontKey():
	f = canvas.defaultFont
	if f.bold: return "%s-bold-%d.pil" % (f.face, f.size)
	else: return "%s-%d.pil" % (f.face, f.size)

def displayForDebugging():
	return       # for faster output, don't display for debugging at all!
	global qdcanvas, canvas
	import piddleQD
	try:
		qdcanvas.clear()
	except:
		qdcanvas = piddleQD.QDCanvas()
	qdcanvas.drawImage( canvas.getImage(), 0, 0 );
	# PATCH...
	bbox = canvas.getImage().getbbox()
	if bbox:
		qdcanvas.drawRect( bbox[0], bbox[1], bbox[2], bbox[3], 
				edgeColor=blue, fillColor=transparent )
	qdcanvas.flush()

def measureAscent():
	reset()
	canvas.drawString("PYTHON", 50, 50)
	displayForDebugging()
	left,top,right,bottom = canvas.getImage().getbbox()
	ascents[fontKey()] = bottom - top

def measureDescent():
	reset()
	canvas.drawString("PTHMygjp_", 50, 50)
	displayForDebugging()
	left,top,right,bottom = canvas.getImage().getbbox()
	key = fontKey()
	descents[key] = bottom - top - ascents[key]

#def measureWidths():
#	w = {}
#	# first get inter-letter spacing
#	reset()
#	canvas.drawString("M", 50, 50)
#	left,top,right,bottom = canvas.getImage().getbbox()
#	M = right - left		# width of one "M"
#	for asciicode in range(33,245):
#		reset()
#		c = chr(asciicode)
#		canvas.drawString(c+'M', 50, 50)
#		displayForDebugging()
#		bbox = canvas.getImage().getbbox()
#		if bbox:
#			left,top,right,bottom = bbox
#			w[c] = right - left - M
#		else:
#			w[c] = 0
#	# special case for handling spaces
#	reset()
#	canvas.drawString("M MM", 50, 50)
#	displayForDebugging()
#	left,top,right,bottom = canvas.getImage().getbbox()
#	w[' '] = right - left - M - 2*w['M']
#	
#	widths[fontKey()] = w

def measureWidths():
	w = {}

	# get widths directly from PIL internals
	import ImageFont
	font = _pilFont(canvas.defaultFont)
	for asciicode in range(32,245):
		c = chr(asciicode)
		m = font.getmask(c)
		w[c] = m.size[0]
	widths[fontKey()] = w

def saveData():
	f = open(os.path.join(_fontprefix,'metrics.dat'), 'wb')
	import cPickle
	cPickle.dump(widths, f, 1)
	cPickle.dump(ascents, f, 1)
	cPickle.dump(descents, f, 1)
	f.close()

for fontname in fonts:
	for size in sizes:
		# measure the plain font
		print "Measuring %s %d plain..." % (fontname, size)
		canvas.defaultFont = Font(face=fontname, size=size)
		measureAscent()
		measureDescent()
		measureWidths()

		# measure the bold version
		print "Measuring %s %d bold..." % (fontname, size)
		canvas.defaultFont = Font(face=fontname, size=size, bold=1)
		measureAscent()
		measureDescent()
		measureWidths()


print "Saving data..."
saveData()
print "All done!"