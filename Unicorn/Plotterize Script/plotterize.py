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
"""Plotterize.py

Generates GCode which from an image (JPEG, GIF, PNG, etc.) for printing with the Unicorn.

More info at: http://wiki.makerbot.com/plotterize

Usage: python plotterize.py [options] file > output.gcode

Options:
  -h, --help						show this help
  --z-feedrate						the Z axis feedrate in mm/min.  default 150
  --z-height						the Z axis print height in mm.  default 0.25
  --xy-feedrate						the XY axes feedrate in mm/min. default 3500
  --width						the maximum width of the build surface in mm. default 80.
  --height						the maximum height of the build surface in mm.  default 80.
  --start-delay						the delay after the pressure valve opens before movement in milliseconds.  default 50
  --stop-delay						the delay after the relief valve opens before movement in milliseconds.  default 150
  --dot-delay						the delay after pressure valve opens for printing a single dot in milliseconds.  default: 50
  --line-width						the width of the line the Frostruder can draw in mm.  default 0.50
  --border						draw a border around your drawing.  default: off
  --stop-distance					the distance to shut down the extruder before the end of a line in mm.  default 1.0
  --invert						invert the image output (light areas are drawn instead of dark areas).  default: off

"""

from math import *
import sys
import getopt
from PIL import Image
from PIL import ImageOps
from PIL import ImageEnhance

class Plotterizer:
	"Class to handle generating frosting code."
	def __init__(self, img_path, z_feedrate, z_height, xy_feedrate, width, height, start_delay, stop_delay, dot_delay, line_width, border, stop_distance, invert):

		self.file = img_path
		self.current_x = 0
		self.current_y = 0
		self.current_z = 0
		
		self.safe_height = 0

		self.z_feedrate = z_feedrate
		self.z_height = z_height
		self.xy_feedrate = xy_feedrate
		self.width = width
		self.height = height
		self.start_delay = start_delay
		self.stop_delay = stop_delay
		self.dot_delay = dot_delay
		self.line_width = line_width
		self.border = border
		self.stop_distance = stop_distance
		self.invert = invert
		self.pbi = 25.4/self.line_width
	
		self.load_image()

	def load_image(self):
		self.image = Image.open(self.file)
		self.image = ImageOps.grayscale(self.image)
		
		brightness = ImageEnhance.Brightness(self.image)
		contrast = ImageEnhance.Contrast(self.image)
	 	self.image = contrast.enhance(20.0)
		self.image = brightness.enhance(2.0)
		
		x_ratio = self.width / float(self.image.size[0])
		y_ratio = self.height / float(self.image.size[1])

		ratio = min(x_ratio, y_ratio)
		
		#multiply so each row = 1 line width
		ratio = ratio / self.line_width

		self.image = self.image.resize((int(self.image.size[0]*ratio), int(self.image.size[1]*ratio)))
		self.image.save(self.file + "-resized.png")
		self.pixels = self.image.load()

		self.width = self.image.size[0] * self.line_width
		self.height = self.image.size[1] * self.line_width

		for i in range(self.image.size[0]):
			for j in range(self.image.size[1]):
				if self.test_pixel(i, j):
					self.pixels[i,j] = 0
				else:
					self.pixels[i,j] = 255
		
		self.image.save(self.file + "-printable.png")
		
		
	def test_pixel(self, x, y):
		if (x >= self.image.size[0]):
			return False
		if (y >= self.image.size[1]):
			return False
				
		#print "pixel at %d, %d = %d" % (x, y, self.pixels[x,y])
		offValue = True
		onValue = False
		if self.invert:
			offValue = False
			onValue = True
		
		if self.pixels[x, y] >= 127:
			return onValue
		else:
			return offValue

	def x_pixel_to_point(self, pixel):
		return -self.width/2 + pixel * self.line_width
	
	def y_pixel_to_point(self, pixel):
		return self.height/2 - pixel * self.line_width
		
	def generate(self):
		"Generate the actual GCode"
		
		print "(Plotterized version of %s)" % (self.file)
		print "(Size: %.2fmm x %.2fmm / %.2f PBI [Peanut Butter Inch])" % (self.width, self.height, self.pbi)
		print "(Call:", " ".join(sys.argv), ")"
		print "G21 (metric ftw)"
		print "G90 (absolute mode)"
		print "G92 X0 Y0 Z0 (zero all axes)"
		self.go_to_point(0, 0, self.z_height, self.z_feedrate)
		print
	
		if self.border:
			min_x = self.x_pixel_to_point(-1)
			max_x = self.x_pixel_to_point(self.image.size[0])
			min_y = self.y_pixel_to_point(self.image.size[1])
			max_y = self.y_pixel_to_point(-1)

			print "(border outline)"
			self.go_to_point(min_x, max_y, self.z_height, self.xy_feedrate)
			print "M300 S30 (pen down)"
			print "G4 P%d (wait %dms)" % (self.start_delay, self.start_delay)
			self.go_to_point(max_x, max_y, self.z_height, self.xy_feedrate)
			self.go_to_point(max_x, min_y, self.z_height, self.xy_feedrate)
			self.go_to_point(min_x, min_y, self.z_height, self.xy_feedrate)
			self.go_to_point(min_x, max_y - self.stop_distance, self.z_height, self.xy_feedrate)
			print "M300 S40 (pen up)"
			self.go_to_point(min_x, max_y, self.z_height, self.xy_feedrate)
			print "G4 P%d (wait %dms)" % (self.stop_delay, self.stop_delay)
			print
		
		for y in range(self.image.size[1]):
			x = 0
			actual_y = self.y_pixel_to_point(y)
			
			self.go_fast_to_point(self.current_x, actual_y, self.z_height, self.xy_feedrate) #added
			print

			while x < self.image.size[0]:
				if (self.test_pixel(x, y)):
					if (self.test_pixel(x+1, y)):
						start = x
						end = x
						while self.test_pixel(end, y):
							end = end+1

						actual_start = self.x_pixel_to_point(start)
						actual_end = self.x_pixel_to_point(end)

						print "(line from %.2f to %.2f at %.2f)" % (actual_start, actual_end, actual_y)
						self.go_to_point(actual_start, actual_y, self.z_height, 3500) #fast feedrate
						print "M300 S30 (pen down)"
						print "G4 P%d (wait %dms)" % (self.start_delay, self.start_delay)
						
						if (abs(actual_end - actual_start) > self.stop_distance):
							self.go_to_point(actual_end-self.stop_distance, actual_y, self.z_height, self.xy_feedrate)
							print "M300 S40 (pen up)"
							self.go_to_point(actual_end, actual_y, self.z_height, self.xy_feedrate)
						else:
							self.go_to_point(actual_end, actual_y, self.z_height, self.xy_feedrate)
							print "M300 S40 (pen up)"
						print "G4 P%d (wait %dms)" % (self.stop_delay, self.stop_delay)
						print

						x = end
					else:
						actual_x = self.x_pixel_to_point(x)
						
						print "(dot at %.2f, %.2f)" % (actual_x, actual_y)
                                                self.go_to_point(actual_x, actual_y, self.z_height, self.xy_feedrate)
						print "M300 S30 (pen down)"
						print "G4 P%d (wait %dms)" % (self.dot_delay, self.dot_delay)
						print "M300 S40 (pen up)"
						print "G4 P%d (wait %dms)" % (self.stop_delay, self.stop_delay)
						print
				x = x+1

		print
		print "(end of print job)"
		print "M300 S40 (pen up)"
		self.go_to_point(self.current_x, self.current_y, 15, self.xy_feedrate)
		self.go_to_point(0, 0, 15, self.xy_feedrate)
		print "M18 (drives off)"
		print "M300 S255 (turn off servo)"
		
	def go_to_point(self, x, y, z, feedrate):
		"Output a move to a point"
		
		print "G1 X%.2f Y%.2f Z%.2f F%.1f" % (x, y, z, feedrate)
		self.current_x = x
		self.current_y = y
		self.current_z = z

	def go_fast_to_point(self, x, y, z, feedrate):
		"Output a move to a point"
		
		print "G1 X%.2f Y%.2f Z%.2f F%.1f" % (x, y, z, 3500)
		self.current_x = x
		self.current_y = y
		self.current_z = z	

def main(argv):
	
	try:
		opts, args = getopt.getopt(argv, "h", [
			"border",
			"dot-delay=",
			"help",
			"height=",
			"invert",
			"line-width=",
			"start-delay=",
			"stop-delay=",
			"stop-distance=",
			"width=",
			"xy-feedrate=",
			"z-feedrate=",
			"z-height="
		])
	except getopt.GetoptError:
		usage()
		sys.exit(2)
        
	z_height = 0.25
	z_feedrate = 150
	xy_feedrate = 1000
	width = 70
	height = 70
	start_delay = 60
	stop_delay = 120
	dot_delay = 50
	line_width = 0.25
	border = False
	stop_distance = 0.0
	invert = False

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
		elif opt in ("--width"):
			width = float(arg)
		elif opt in ("--height"):
			height = float(arg)
		elif opt in ("--start-delay"):
			start_delay = float(arg)
		elif opt in ("--stop-delay"):
			stop_delay = float(arg)
		elif opt in ("--dot-delay"):
			dot_delay = float(arg)
		elif opt in ("--line-width"):
			line_width = float(arg)
		elif opt in ("--border"):
			border = True
		elif opt in ("--stop-distance"):
			stop_distance = float(arg)
		elif opt in ("--invert"):
			invert = True
		
	frosty = Plotterizer(argv[-1], z_feedrate, z_height, xy_feedrate, width, height, start_delay, stop_delay, dot_delay, line_width, border, stop_distance, invert)
	frosty.generate()

def usage():
    print __doc__

if __name__ == "__main__":
	main(sys.argv[1:])
