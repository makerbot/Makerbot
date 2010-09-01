from math import *
import sys

class GCodeContext:
    def __init__(self, z_feedrate, z_height, xy_feedrate, start_delay, stop_delay, line_width, file):
        
	self.z_feedrate = z_feedrate
	self.z_height = z_height
	self.xy_feedrate = xy_feedrate
	self.start_delay = start_delay
	self.stop_delay = stop_delay
	self.line_width = line_width
	self.file = file
	
	self.drawing = False
	self.last = None
	self.codes = []

    def generate(self):
	print "(Scribbled version of %s @ %.2f)" % (self.file, self.xy_feedrate)
	print "(", " ".join(sys.argv), ")"
	print "G21 (metric ftw)"
	print "G90 (absolute mode)"
	print "G92 X0 Y0 Z0 (zero all axes)"
	print "G92 Z%0.2F F150.00 (go up to printing level)" %self.z_height
	print

	for line in self.codes:
		print line
	
	print
	print "(end of print job)"
	print "M300 S50"
	print "G4 P%d (wait %dms)" % (self.stop_delay, self.stop_delay)
	print "G1 X0 Y0 F3500.00"
	print "G92 Z15 F150.00 (go up to finished level)"
	print "G92 X0 Y0 Z15 F150.00 (go up to finished level)"
	print "M18 (drives off)"

    def start(self):
		self.codes.append("M300 S40 (pen down)")
		self.codes.append("G4 P%d (wait %dms)" % (self.start_delay, self.start_delay))
		self.drawing = True

    def stop(self):
		self.codes.append("M300 S50 (pen up)")
		self.codes.append("G4 P%d (wait %dms)" % (self.stop_delay, self.stop_delay))
		self.drawing = False

    def go_to_point(self, x, y, stop=False):
        if self.last == (x,y):
            return
        if stop:
                return
        else:
                if self.drawing: 
                    self.codes.append("M300 S50 (pen up)") 
                    self.codes.append("G4 P%d (wait %dms)" % (self.stop_delay, self.stop_delay))
                    self.drawing = False
                    
		self.codes.append("G1 X%.2f Y%.2f F%.2f" % (x,y, self.xy_feedrate))

	self.last = (x,y)
	
    def draw_to_point(self, x, y, stop=False):
        if self.last == (x,y):
            return
        if stop:
		return
        else:
                if self.drawing == False:
                    self.codes.append("M300 S40 (pen down)")
                    self.codes.append("G4 P%d (wait %dms)" % (self.start_delay, self.start_delay))
                    self.drawing = True
                    
		self.codes.append("G1 X%.2f Y%.2f F%.2f" % (x,y, self.xy_feedrate))

	self.last = (x,y)
