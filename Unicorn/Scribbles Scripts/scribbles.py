#!/usr/bin/python
#
# Copyright (c) 2010 MakerBot Industries
# 
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
#
"""
scribbles.py
Derived from lunchlines.py used for the Frostruder:

Generates GCode from a DXF file for printing with the Frostruder.

More info at: http://wiki.makerbot.com/lunchlines

Usage: python lunchlines.py [options] file > output.gcode

Options:
  -h, --help						show this help
  --z-feedrate						the Z axis feedrate in mm/min.  default 150
  --z-height						the Z axis print height in mm.  default 0.25
  --xy-feedrate						the XY axes feedrate in mm/min. default 3500
  --start-delay						the delay after the pressure valve opens before movement in milliseconds.  default 50
  --stop-delay						the delay after the relief valve opens before movement in milliseconds.  default 150
  --line-width						the width of the line the Frostruder can draw in mm.  default 0.50
  --stop-distance					the distance to shut down the extruder before the end of a line in mm.  default 1.0
"""

from math import *
import sys
import getopt
from scribbles.import_dxf import DxfParser
from scribbles.context import GCodeContext

def main(argv):
	try:
		opts, args = getopt.getopt(argv, "h", [
			"help",
			"line-width=",
			"start-delay=",
			"stop-delay=",
			"stop-distance=",
			"xy-feedrate=",
			"z-feedrate=",
			"z-height="
		])
	except getopt.GetoptError:
		usage()
		sys.exit(2)
        
	z_height = 0
	"0.25"
	z_feedrate = 150
	"150"
	xy_feedrate = 2000
	"3500"
	start_delay = 60
	"50"
	stop_delay = 120
	"150"
	line_width = 0.5
	"0.50"
	stop_distance = 0.0
	"1.0"

	for opt, arg in opts:
		if opt in ("-h", "--help"):
			usage()
			sys.exit()
		elif opt in ("--z-feedrate"):
			z_feedrate = float(arg)
		elif opt in ("--z-height"):
			z_height = float(arg)
		elif opt in ("-xy-feedrate"):
			xy_feedrate = float(arg)
		elif opt in ("--start-delay"):
			start_delay = float(arg)
		elif opt in ("--stop-delay"):
			stop_delay = float(arg)
		elif opt in ("--line-width"):
			line_width = float(arg)
		elif opt in ("--stop-distance"):
			stop_distance = float(arg)

	parser = DxfParser(open(argv[-1], 'r'))
	context = GCodeContext(z_feedrate, z_height, xy_feedrate, start_delay, stop_delay, line_width, stop_distance, argv[-1])
	parser.parse()
	for entity in parser.entities:
		entity.get_gcode(context)
	context.generate()

if __name__ == "__main__":
	main(sys.argv[1:])
else:
    raise RuntimeError("lunchlines.py is the top-level script, and is not meant to be imported.")



