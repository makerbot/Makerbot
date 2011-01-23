# v1.0 Jordan Miller, jmil@benchscience.org
# http://www.thingiverse.com/thing:5650

# This program requires python and can be run on any platform

# The call is "python RAPID_REVERSALify.py FILE.gcode printRPM reversalRPM waitTime"
# Where FILE.gcode is the complete path and gcode you want to process.
# For testing, use this command, without the quotes:
# python RAPID_REVERSALify.py oozebane.gcode 2.857 25 200

# First, every M103 command is replaced with:
# M103 (Extruder off)
# M108 R25
# M102 (Extruder on, RAPID REVERSAL)
# G04 P200 (Wait t/1000 seconds)
# M103 (Extruder off)
# 
# Then, every M101 command is replaced with:
# (reaccelerate to prev position)
# M108 R25
# M101 (Extruder on, RAPID FORWARD)
# G04 P200 (Wait t/1000 seconds)
# M103 (Extruder off)
# M108 R2.3
# M101 (Extruder on, forward)


##### NEED TO FIX DIVISION OPERATOR!!!!!
from __future__ import division
#http://docs.python.org/release/2.2.3/whatsnew/node7.html

printRPM = 2.0      # regular RPM flow rate used for printing
reversalRPM = 25.0     # RPM to rapid reverse and rapid forward
waitTime = 200  # number of milliseconds to wait at reversalRPM for reverse and forward

import sys
import re


# for arg in sys.argv: 
	# print arg


sourceGcodeFilename = sys.argv[1]
# maxRPM = sys.argv[2]
# factor = float(maxRPM) / 255
destinationFilename = sourceGcodeFilename[:-6] + "_RAPIDREVERSAL.gcode"
# print destinationFilename
printRPM = sys.argv[2]
print "we will print at " + str(printRPM) + " RPM"
reversalRPM = sys.argv[3]
print "we will rapid reverse at " + str(reversalRPM) + " RPM"
waitTime = sys.argv[4]
print "we will wait for " + str(waitTime) + " ms during rapid reversal"


fileIN = open(sourceGcodeFilename, "r")
FILEOUT = open(destinationFilename,"w")


line = fileIN.readline()

# READ THE ENTIRE GCODE ONE LINE AT A TIME, PROCESS it, WRITE OUT RPMified code, w00t!
while line:
	
	RPMifiedLine = line
	
	if RPMifiedLine == "M103\n":		
		RPMifiedLine = "" \
			+ "M103 (Extruder off)\n" \
			+ "M108 R" + str(reversalRPM) + "\n" \
			+ "M102 (Extruder on, RAPID REVERSAL)\n" \
			+ "G04 P" + str(waitTime) + " (Wait t/1000 seconds)\n" \
			+ "M103 (Extruder off)\n"
		
	elif RPMifiedLine == "M101\n":
		RPMifiedLine = "" \
			+ "(reaccelerate to prev position)\n" \
			+ "M108 R" + str(reversalRPM) + "\n" \
			+ "M101 (Extruder on, RAPID FORWARD)\n" \
			+ "G04 P" + str(waitTime) + " (Wait t/1000 seconds) \n" \
			+ "M103 (Extruder off)\n" \
			+ "M108 R" + str(printRPM) + "\n" \
			+ "M101 (Extruder on, forward)\n"

	FILEOUT.writelines(RPMifiedLine)
	
	line = fileIN.readline()
