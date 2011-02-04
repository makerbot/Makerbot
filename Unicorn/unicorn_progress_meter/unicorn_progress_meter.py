# Script that adds extra commands to your gcode file to drive the
# unicorn progress meter.

# What's a unicorn progres meter, you ask? It's a unicorn connected
# to the servo output on your Gen4 electronics, that moves a little
# arrow to show your build progress. It's a simple hack based on the
# number of lines in your program, so don't expect the progress bar
# to be too consistant.

# Designed by Matt Mets in February, 2011. Released under the WTFPL

import sys

sourceGcodeFilename = sys.argv[1]
destinationFilename = sourceGcodeFilename[:-6] + "_PROGRESS.gcode"


def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1

# first, get length of file:
length = file_len(sourceGcodeFilename)

# now, step through and start inserting stepper commands at opportune times
linesPerPercent =  length/180;

outfile = open(destinationFilename, "w")

with open(sourceGcodeFilename) as f:
    for i, l in enumerate(f):
        outfile.write(l)
        
        if (i%linesPerPercent == 0):
            outfile.write("M300 S" + str(i/linesPerPercent) + "\n")
