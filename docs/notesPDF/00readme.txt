Andy Robinson 23:13 06/10/99,

[updated 5 Feb. 2000 by Piddle maintainer chris lee]

This is the latest PDF back end for PIDDLE.  

If you are looking for a complete PIDDLE distribution, it
can be found at piddle.sourceforge.net.  Joe Strout
incorporates my releases each time.  If you are a PIDDLE 
user, you should only use this if you need a patch urgently, 
and Joe has not yet had time to include it in his distribution.



Release Note:
-------------
There has been a major reorganisation so a few notes are 
in order.  First, the modules:

"piddlePDF.py" is the PDF back end.  To do pure PIDDLE drawings,
this is all you will use directly.  It now aims ONLY to support 
the standard PIDDLE API calls.  To access PDF-specific features,
you call methods of its 'self.pdf' attribute, which is an instance
of pdfgen.Canvas (see below).  The vast majority of its methods
don't make direct PDF, but use the low-level canvas; this means
that we could soon extend the low-level canvas to make Postscript 
too.  This means that code using pdf-specific features will break;
usually you just need to change MyCanvas.foo() to MyCanvas.pdf.foo()
to fix it.

"pdfgen.py" is a lower-level graphics canvas which closely follows 
the PostScript imaging model.  It has NO dependencies at all on
PIDDLE.  pdfgen.Canvas thinks in terms of PostScript font names, 
RGB values, coordinate transforms and paths.  It now produces 
efficient PDF, much faster than before with less state changes.  
It also exposes 'Path Objects' which shoudl allow a sensible handling
of clipping paths in the next release. 
New PDF features will be exposed here. Again, this is a complete API 
and you do not need to use the modules below here unless keen to get 
involved in the source.

"testpdfgen.py" checks it works OK and shows examples of some
features.

"pdfdoc.py" handles the outer layer of PDF - objects to represent
pages, streams etc., linking them and writing to disk.  It is
still very 'hard-coded' and needs a cleanup before we can add new
objects, but works fine.

"pdfutils.py" includes utility functions for image and stream
processing; this will grow as we do more image enhancements
Robert Kern is working on an extension module to do some of this;
we may be able to arrange things so that it uses a C extension
module if available, or goes slowly if not.

"pdfgeom.py" includes math functions which do not depend on anything
but the Python library.  Currently just Robert's bezierArc function,
but coordinate transforms and stacks are coming soon.  This might
be useful for other PIDDLE back ends, hence breaking it out.


Still to do:
-----------
This is only about half of the promised upgrade.  Next on the list are:
- page compression options
- document outlines
- clipping and character paths
- tracking the text cursor through coordinate transformations

[Ed. note: The above features have been added to the release as of Piddle 1.0. -cwl]


Regards,

Andy


