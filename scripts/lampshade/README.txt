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

You can get usage information by running:
python ./lampshade.py -h

The demo files in the patterns directory were made with the following
parameters:

python ./lampshade.py -c --rtop=23 --rbot=30 -H 80 patterns/earth.png >patterns/earth.gcode

python ./lampshade.py -c -r 30 -H 60 patterns/fleur.png >patterns/fleur.gcode

python /lampshade.py -c -r 30 -H 80 patterns/tiles.png >patterns/tiles.gcode

The "-c" flag is important if you want to do "seamless" (spiral) prints.
Older versions of the firmware and ReplicatorG didn't support continuous
concurrent Z motion well, and so this was not the default at the time the
script was written.

New in the latest version of the script is the "bottom-layers" parameter.
This will close the bottom of the shade with a spiral bottom, giving you a
cup.  (This feature was used to create the records in our April Fool's Day
prank.)

Good luck, and have fun!
-a
