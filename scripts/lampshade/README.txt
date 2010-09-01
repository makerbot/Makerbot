********************
*** LAMPSHADE.PY ***
********************

Lampshade.py is a simple script for generating gcode for printing
simple lampshades based on a bitmap.  The wall thickness of the
lampshade at any point is proportional to the darkness of the
corresponding pixel in the originating bitmap.  More light will tend
to shine through lighter areas.

To run lampshade.py, you'll need a modern version of python (anything
after 2.3 should do) and the Python Imaging Library (PIL), available
from:
http://www.pythonware.com/products/pil/



You can get a list of parameters and help
python ./lampshade.py -h

The demo files in the patterns directory were made with the following
parameters:

python ./lampshade.py --rtop=23 --rbot=30 -H 80 patterns/earth.png >patterns/earth.gcode

python ./lampshade.py -r 30 -H 60 patterns/fleur.png >patterns/fleur.gcode

Good luck, and have fun!
-a
