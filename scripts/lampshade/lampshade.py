#!/usr/bin/python
import math
import sys
import Image

im = Image.open(sys.argv[1]).convert("L")
pixels = im.load()

layerHeight = 0.33

rBottomMm = 30.0
rTopMm = 30.0
heightMm = 40.0

segments = max(20,im.size[0])

prefix = """
(Cupcake ABS default skeinforge profile)
(homing routing)
M104 S220 T0 (Temperature to 220 celsius)
G21 (Metric FTW)
G90 (Absolute Positioning)
G92 X0 Y0 Z0 (You are now at 0,0,0)
(You have failed me for the last time, MakerBot)
G0 Z15 (Move up for test extrusion)
M108 S255 (Extruder speed = max)
M6 T0 (Wait for tool to heat up)
G04 P5000 (Wait 5 seconds)
M101 (Extruder on, forward)
G04 P5000 (Wait 5 seconds)
M103 (Extruder off)
M01 (The heater is warming up and will do a test extrusion.  Click yes after you have cleared the nozzle of the extrusion.)
G0 Z0	(Go back to zero.)
(end of start.)
"""

suffix = """
(end of the file, cooldown routines)
M104 S0
G91
G1 Z10
"""

feedrateInMmPerS = 34.5

maxAdjustment = 0.4

# Do not edit

layerCount = heightMm / layerHeight
rDeltaPerLayer = (rTopMm - rBottomMm)/layerCount
anglePerSegment = 2*math.pi/segments

baseFeedrate = feedrateInMmPerS * 60.0

def getXYZ(layer,segment):
    r = rBottomMm + (rDeltaPerLayer*layer)
    angle = anglePerSegment * segment
    z = layerHeight * layer
    x = math.sin(angle) * r
    y = math.cos(angle) * r
    return (x,y,z)

def makeSegment(layer, segment, value, earlyShutoff = 0):
    feedrate = baseFeedrate * ((value * maxAdjustment) + ((1.0-value)*1.0))
    start = getXYZ(layer, segment-1)
    end = getXYZ(layer,segment)
    return "G1 X%f Y%f Z%f F%f" % (end[0],end[1],end[2],feedrate)

def makeShape():
    print prefix
    print "M101"
    for layer in range(0,int(layerCount)):
        for segment in range(0, segments):
            x = segment
            y = int(float(im.size[1]*layer)/layerCount)
            print makeSegment(layer, segment, pixels[x,y]/256.0)
    print "M103"
    print suffix


makeShape()
