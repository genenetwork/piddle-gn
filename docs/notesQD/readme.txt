piddleQD is the QuickDraw backend to PIDDLE.  It only runs under MacOS,
and requires at least version 1.5.2c1 of MacPython.

-------------------- QDRotate -------------------
It also requires a little extension library to provide support for rotated
strings.  That's included in this folder as "QDRotate.sit.hqx".

1. Unpack QDRotate.sit.hqx using StuffIt Expander.

2. Place the QDRotate.ppc.slb inside your "Python 1.5.2c1:Mac:PlugIns" folder.

To test, launch Python (the IDE or the PythonInterpreter, either one) and 
enter "import QDRotate".  If you don't get an error, then it's installed and
you're good to go.

piddleQD will work without QDRotate as long as you don't try to draw any
rotated strings -- as soon as you do, it will raise an exception.

-------------------- PixMapWrapper -------------------
Finally, to use the drawImage() command, you need a little helper module
called PixMapWrapper.  That's also included in this folder; just put it
somewhere in your Python path.

Note that there is a bug here somewhere, which can sometimes cause
drawImage() to draw to the wrong port (like your Python editor window).
This is a nuisance, but not actually dangerous.  I'll try to fix it in
future versions.


If you have any questions or problems, contact joe@strout.net.

Cheers,
-- Joe
10/21/99
