"""
PiddlifyAI takes an Abode Illustrator file and outputs to a PiddleVCR file
which can then be used by some of the other Piddle back ends. Since the VCR 
output is in the form of bezier points not all the backends will be able 
to use it.
"""

import	sys
import string
import os

StandardEnglishFonts = [
    'Courier', 'Courier-Bold', 'Courier-Oblique', 'Courier-BoldOblique',  
    'Helvetica', 'Helvetica-Bold', 'Helvetica-Oblique', 
    'Helvetica-BoldOblique',
    'Times-Roman', 'Times-Bold', 'Times-Italic', 'Times-BoldItalic',
    'Symbol','ZapfDingbats']

lineEnd = '\n'


class Piddify:
	
	def __init__(self):
		self.output = ['piddleVCR 0.1' + lineEnd]
		self.size = []
		self.start = []
		self.figure = []
		self.text = 0
		self.sText = []
		self.fontenc = 0
		
	def work(self, file):
		""" Check the input is the right sort of file and write the output""" 
		if file[-3:] == '.ai':
			outfile = file[:-2] + 'vcr'
		elif file[-4:] == '.art':
			outfile = file[:-3] + 'vcr'
		else:
			outfile = file  + 'vcr'
			
		f = open(file, 'r')
		input = f.readlines()
		f.close()
		line = string.split(input[0])
		if line[0][:4] <> '%!PS':
			print 'This is not a suitable file'
			sys.exit(1)
		elif  len(line) > 1 and  line[1][:4] == 'EPSF':
			print 'This is not a suitable file'
			sys.exit(1)
			
		for line in input:
#			print line
			if line[0] == '%':
				self.header(line)
			elif line[:5] == 'Adobe':
				pass
			else:
				self.body(line)
		
		self.output.append('END')
		f = open(outfile, 'w')
		f.writelines(self.output)
		f.close()
		
		
	def header(self, line):
		"""Extract information from the AI header"""
		line = string.split(line)
		if line[0] == '%AI5_RulerUnits:':
			self.units = line[1]
#			print self.units
		elif line[0] == '%%BoundingBox:':
			self.size = line[1:]

	def body(self, line):
		"""Extract needed information from the file body"""
#		print line
		if line == '[\n':
			self.fontenc = 1
			return
		line = string.split(line)
		if self.start:
			self.bodym(line)
		elif self.text:
			self.bodyTo(line)
		elif self.fontenc:
			self.bodyFE(line)
		else:
			try:
				if line[-1][0] == '*':line[-1] = '1'+ line[-1][1]
				eval('self.body%s(%s)' % (line[-1], line))
			except AttributeError:
#				print 'Not yet impemented: self.body%s' % line[-1]
				print 'def body%s(self, line):' % line[-1]

#######################################################################
	"""Methods for obtaining colours"""
	
	def colorConvert(self, line):
		ln =  map(lambda x: string.atof(x), line[:4])
		red = 1 - min(1, ln[0] + ln[3])
		green = 1 - min(1, ln[1] + ln[3])
		blue = 1 - min(1, ln[2] + ln[3])
		return red, green, blue		
			
	def bodyK(self, line):
		self.lineColor = 'Color(%s, %s, %s)' % self.colorConvert(line)

	def bodyk(self, line):
		self.fillColor = 'Color(%s, %s, %s)' % self.colorConvert(line)

	def bodyXA(self, line):
		self.lineColor = 'Color(%s, %s, %s)' % line

	def bodyXa(self, line):
		self.fillColor = 'Color(%s, %s, %s)' % line
		
	def bodyg(self, line):
		line = ['0','0','0'] + line
		self.fillColor = 'Color(%s, %s, %s)' % self.colorConvert(line)

	def bodyG(self, line):
		line = ['0','0','0'] + line
		self.lineColor = 'Color(%s, %s, %s)' % self.colorConvert(line)


#######################################################################
	"""Line Weight"""
	
	def bodyw(self, line):
		self.lineWidth = line[0]

#######################################################################
	"""Don't need font encodings"""
	
	def bodyFE(self, line):
		if line[0] == 'TE':
			self.fontenc = 0

#######################################################################
	"""Methods for obtaining text information"""
	
	def bodyTo(self, line):
		self.text = 1
		if line[-1] == 'Tp':
			self.textStart(line[:-1])
		elif line[-1] == 'Tf':
			self.textFont(line[:-1])
		elif line[-1] == 'Tx' or line[-1] == 'Tj':
			self.textTxt(line[:-1])
		elif line[-1] == 'TO':
			self.drawString()
			self.text = 0
			self.sText = []
		else:
			return

	def textStart(self, line):
		a,b,c,d,x1,y1,sp = line
		self.position = x1, y1, 0

	def textFont(self, line):
		bd = it = 0
		ft, sz = line
		ft = string.split(ft[2:], '-')
		print ft
		if len(ft) > 1:
			if ft[1][0] == 'B': bd = 1
			if ft[1][0] == 'I' or ft[1][0] == 'O': it = 1
			if len(ft[1]) > 4:
				if ft[1][4] == 'I' or ft[1][4] == 'O': it = 1
		
		self.font = ft[0], bd, it, sz
		print self.font
			
	def textTxt(self, line):
		line = string.join(line)
		line = string.replace(line[1:-1],"\'", "\\'")
		line = string.replace(line,'''\"''', '''\\"''')
		self.sText.append(line)
		
	def drawString(self):
		print self.position
		self.position = self.transform([self.position[0], self.position[1]]), 0
		self.position[0][1] = self.position[0][1] + string.atof(self.font[3])
		code = "drawString('%s',%s,%s,Font(face='%s',bold=%s,italic=%s,size=%s),%s)"
		for line in self.sText:
			data = (line, self.position[0][0], self.position[0][1],\
				self.font[0],self.font[1],self.font[2],self.font[3],self.position[1])
			data = code % data
			self.position[0][1] = self.position[0][1] + string.atof(self.font[3])
			self.output.append(data + lineEnd)
			
#######################################################################
	"""Methods for obtaining line and point information"""
	

	def bodym(self, line):
		if line[-1] == 'S':
			self.bodyS()
		elif line[-1] == 's':
			self.bodys()
		elif line[-1] == 'F':
			self.bodyF()
		elif line[-1] == 'f':
			self.bodyf()
		elif line[-1] == 'B':
			self.bodyB()
		elif line[-1] == 'b':
			self.bodyb()
		else:
			self.start.append(self.transform(line[:-1]))
			self.figure.append(line[-1])
		
	def bodyS(self):
		self.drawCurve(1, 0, 0)
		self.start = []
		self.figure = []

	def bodys(self):
		self.drawCurve(1, 0, 1)
		self.start = []
		self.figure = []

	def bodyB(self):
		self.drawCurve(1, 1, 0)
		self.start = []
		self.figure = []

	def bodyb(self):
		self.drawCurve(1, 1, 1)
		self.start = []
		self.figure = []

	def bodyF(self):
		self.drawCurve(0, 1, 0)
		self.start = []
		self.figure = []

	def bodyf(self):
		self.drawCurve(0, 1, 1)
		self.start = []
		self.figure = []

	def drawCurve(self, line, fill, closed):
		if len(self.figure) == 1: return
		if line:
			line = self.lineColor
		else:
			line = 'Color(-1,-1,-1)'			
		if fill:
			fill = self.fillColor
		else:
			fill = 'Color(-1,-1,-1)'
		
		pl = 'drawcCurve(['
		ptlist = self.pointList()		
		ln = '], %s,%s,%s,%s)' % (line, self.lineWidth, fill, closed)
		self.output.append(pl + ptlist + ln + lineEnd)
		
	def pointList(self):
		pt = 0
		ptlist = ''		
		while pt < len(self.figure):
			code = '(%s,%s,%s,%s,%s,%s)'
			if self.figure[pt] == 'm':
				x1, x2 = tuple(self.start[pt])
				code = '(%s,%s)'	
				data = (x1,x2)
			if self.figure[pt] == 'c' or self.figure[pt] == 'C':
				x1,x2, x3,x4,x5,x6 = tuple(self.start[pt])
				data = (x1,x2,x3,x4,x5,x6)
			elif self.figure[pt] == 'v' or self.figure[pt] == 'V':
				x1, x2 = tuple(self.start[pt-1][-2:])
				x3,x4,x5,x6 = tuple(self.start[pt])
				data = (x1,x2,x3,x4,x5,x6)
			elif self.figure[pt] == 'y' or self.figure[pt] == 'Y':
				x1,x2,x3,x4 = tuple(self.start[pt])
				data = (x1,x2,x3,x4,x3,x4)
			elif self.figure[pt] == 'l' or self.figure[pt] == 'L':
				x1, x2 = tuple(self.start[pt-1][-2:])
				x3,x4 = tuple(self.start[pt])
				data = (x1,x2,x3,x4,x3,x4)
			pts = code % data
			ptlist = ptlist + pts + ', '
			pt = pt + 1
		return ptlist[:-2]

#######################################################################
	"""Methods for information we can't use"""
	
		
	def bodyAr(self, line):pass
	def bodyJ(self, line):pass
	def bodyLB(self, line):pass
	def bodyLb(self, line):pass
	def bodyLn(self, line):pass
	def bodyM(self, line):pass
	def bodyR(self, line):pass
	def bodyU(self, line):pass
	def bodyXR(self, line):pass
	def bodyd(self, line):pass
	def bodyi(self, line):pass
	def bodyj(self, line):pass
	def bodyshowpage(self, line):pass
	def bodyu(self, line):pass
	def body1u(self, line):pass
	def body1U(self, line):pass
	def bodyTE(self, line):pass
	def bodyO(self, line):pass
	def bodyTZ(self, line):pass
	def bodyA(self, line):pass
	def bodyD(self, line):pass


#######################################################################
	"""Utilty Methods"""
	
	def transform(self, line):
		start = []
		bb = map(lambda x: string.atof(x), self.size)
		x1, y1, x2, y2 = bb
		ht = y2 - y1
#		print line
		st =  map(lambda x: string.atof(x), line)
		even = range(0,len(st),2)
		list = []
		for x in even:
			ls = [st[x] - x1, y2-st[x+1]]
			list = list + ls
		return list

#######################################################################
	"""This makes it all work nicely on a mac."""
	

def getlist():
	if os.name == 'mac':
		import macfs

		while 1:
			fss, ok = macfs.PromptGetFile('Which AI file to use?')
			if not ok:
				sys.exit(1)
			my_file = (fss.as_pathname())
			return my_file
	else:
		print "Sorry can't do that without a mac"


def run():
	try:
		a = sys.argv[1]
	except IndexError:
		a = getlist()
	p = Piddify()
	p.work(a)
	
	
if __name__=="__main__":  
	run()
#	sys.exit(1)
