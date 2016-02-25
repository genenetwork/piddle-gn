import piddle
import math

def makeCanvas():
        "Create a Canvas object."
        import piddleAI
        return piddleAI.AICanvas(name='Sample2.ai')

def plot(f,canvas,offset=0):
        for i in range(0,100):
                x = float(i)/100
                canvas.drawLine(i*3+offset,250, i*3+offset,250-100*f(x))

def showColors(colors):
        global canvas
        try:
                canvas.clear()
        except:
                canvas = makeCanvas()

        # draw a black background for the spectrum
        canvas.drawRect( 0,0,300,100, edgeColor=piddle.black, fillColor=piddle.black )

        # draw the spectrum
        for i in range(len(colors)):
                canvas.drawLine(i,20,i,80, colors[i])

        # plot the components of the spectrum
        canvas.defaultLineColor = piddle.red
        plot(redfunc, canvas)

        canvas.defaultLineColor = piddle.blue
        plot(bluefunc, canvas, 1)

        canvas.defaultLineColor = piddle.green
        plot(greenfunc, canvas, 2)

        # update the canvas
        canvas.flush()

def bluefunc(x):
        return 1.0 / (1.0 + math.exp(-10*(x-0.6)))

def redfunc(x):
        return 1.0 / (1.0 + math.exp(10*(x-0.5)))

        return out

def greenfunc(x):
        return 1 - pow(redfunc(x+0.2),2) - bluefunc(x-0.3)

def genColors(n=100):
        out = [None]*n;
        for i in range(n):
                x = float(i)/n
                out[i] = piddle.Color(redfunc(x), greenfunc(x), bluefunc(x));
        return out

showColors(genColors(300))

