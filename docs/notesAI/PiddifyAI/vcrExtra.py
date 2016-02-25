from piddle import *
from piddlePDF import *
from piddleVCR import *
from pdfcatpref import *
#import pdfText
import sys
import stringformat
import string
import re
import time
import macpath
from types import *

class VCRcat(VCRCanvas):

	def drawcCurve(self, pointlist, 
				edgeColor=None, edgeWidth=None, fillColor=None, closed=0):
		"Draw a list of abitary BÈzier curves with control points x1,y1 to x4,y4."

		self._recordfunc("drawcCurve", pointlist,edgeColor,edgeWidth,fillColor,closed)

	def playBack(self, canvas):
		for item in self.recording:
#			print item
			exec("canvas." + item)
#		canvas.flush()
	


class PDFcat(PDFCanvas):
	
		
	def drawcCurve(self, pointlist,
			edgeColor=None, edgeWidth=None, fillColor=None, closed=0):

		self._updateFillColor(fillColor)
		self._updateLineWidth(edgeWidth)
		self._updateLineColor(edgeColor)
		if self._currentLineColor != transparent:
			if closed:
				if self._currentFillColor != transparent:
					op = 'b*'    #closepath, eofill, stroke
				else:
					op = 's'  # closepath and stroke
			else:
				if self._currentFillColor != transparent:
					op = 'B*'    #eofill, stroke
				else:
					op = 'S'  # stroke
		else:
			op  = 'f'
		x= 0
#		print pointlist
#		print len(pointlist)
		while x<len(pointlist):
			if x == 0:
				codeline = '%s -%s m '
				data = pointlist[0]
			else:
				codeline = '%s -%s %s -%s %s -%s c '
				data = pointlist[x]
			x = x+1
#			print codeline % data
			self.code.append(codeline % data)
		self.code.append(op)


