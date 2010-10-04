#!/usr/bin/python

# lampshade.py
# Copyright 2010 Makerbot Industries LLC
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from optparse import OptionParser
import math
import sys
import Image

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

suffixABP = """
(end of the file, cooldown routines)
G1 X0 Y50 F3300.0 (move to ejection position)
M106 (conveyor on)
G04 P10000 (wait 10 seconds)
M107 (conveyor off)
G1 X0 Y0 F3300.0 (recenter platform)
G1 X0 Y0 Z0 F3300.0 (recenter platform)
M104 S0 (shut off extruder if last cycle)
(CYCLE BEGINS ANEW)
"""


# Do not edit

def makeSpiralPoints(radius):
    "Returns an array of points defining a spiral from the inside out"
    global extrusionWidth
    segmentLen = 2.0
    last = (0,0)
    points = [last]
    theta = math.pi/2
    r = theta * extrusionWidth / (2*math.pi)
    while r <= radius:
        points.append( (r*math.cos(theta), r*math.sin(theta)) )
        tDelta = math.atan( segmentLen / r )
        theta = theta + tDelta
        r = theta * extrusionWidth / (2*math.pi)
    return points

def makeBottom(layer):
    "Generate a spiral bottom"
    global rBottomMm
    z = layerHeight * layer
    points = makeSpiralPoints(rBottomMm+extrusionWidth)
    if (layer % 2) == 0:
        points.reverse()
    for p in points:
        print "G1 X%f Y%f Z%f F%f" % (p[0],p[1],z,baseFeedrate)

def init():
    global layerCount, rDeltaPerLayer, anglePerSegment
    global baseFeedrate
    global segments
    layerCount = heightMm / layerHeight
    rDeltaPerLayer = (rTopMm - rBottomMm)/layerCount
    anglePerSegment = 2*math.pi/segments
    baseFeedrate = feedrateInMmPerS * 60.0

def getXYZ(layer,segment,roff=0.0):
    global continuous
    global bottom
    r = rBottomMm + (rDeltaPerLayer*layer)
    angle = anglePerSegment * segment
    z = bottom + (layerHeight * layer)
    if continuous:
        z = z + (layerHeight * (float(segment)/segments))
    x = -math.sin(angle) * r
    y = math.cos(angle) * r
    return (x,y,z)

def makeSegment(layer, segment, value, earlyShutoff = 0):
    invvalue = 1.0-value
    feedrate = baseFeedrate * ((invvalue * maxAdjustment) + value)
    start = getXYZ(layer, segment-1)
    end = getXYZ(layer,segment)
    return "G1 X%f Y%f Z%f F%f" % (end[0],end[1],end[2],feedrate)

def makeShape():
    print prefix
    print "M101"
    print "(Base)"
    for i in range(0,bottomLayers):
        makeBottom(i)
    if bottomLayers > 0:
        # add single-layer seal
        print "(Adding seal along bottom)"
        for segment in range(0, segments):
            r = rBottomMm - extrusionWidth
            angle = anglePerSegment * segment
            z = bottom + layerHeight
            x = -math.sin(angle) * r
            y = math.cos(angle) * r
            print "G1 X%f Y%f Z%f F%f" % (x,y,z,baseFeedrate)
    print "(Sides)"
    for layer in range(0,int(layerCount)):
        for segment in range(0, segments):
            x = segment
            y = (im.size[1] - int(float(im.size[1]*layer)/layerCount)) - 1
            print makeSegment(layer, segment, pixels[x,y]/256.0)
    print "M103"
    if abp:
        print suffixABP
    else:
        print suffix


usage = "usage: %prog [options] image.png"
parser = OptionParser(usage = usage)
parser.add_option("-r","--radius",type="float",dest="radius",
                  help="set the top and bottom radius of a right cylinder")
parser.add_option("-l","--layerheight",type="float",dest="layerheight",
                  help="set the height of a single layer, in mm",
                  default=0.33)
parser.add_option("--rtop",type="float",dest="rtop", 
                  help="set the top radius of a conical shade",
                  default=30.0)
parser.add_option("--rbot",type="float",dest="rbot",
                  help="set the bottom radius of a conical shade",
                  default=30.0)
parser.add_option("-H","--height",type="float",dest="height",
                  help="set the height of the shade",
                  default=40.0)
parser.add_option("-c","--continuous",action="store_true",dest="continuous",
                  help="use continuous Z movement",
                  default=False)
parser.add_option("-a","--ABP",action="store_true",dest="abp",
                  help="use automated build platform",
                  default=False)
parser.add_option("--bottom-layers",type="int",dest="bottom",
                  help="number of layers in the floor",
                  default=0)
parser.add_option("-f","--feedrate",type="float",dest="feedrate",
                  help="set the base feedrate",
                  default=34.5)
#parser.add_option("--rexp",type="string"
(options,args) = parser.parse_args()

if len(args) != 1:
    print "Please provide exactly one filename as an argument."
    parser.print_help()
    exit()

extrusionWidth = 0.5
bottomLayers = options.bottom
rBottomMm = options.rbot
rTopMm = options.rtop
layerHeight = options.layerheight
heightMm = options.height
feedrateInMmPerS = options.feedrate
if options.radius:
    rBottomMm = options.radius
    rTopMm = options.radius
maxAdjustment = 0.49
continuous = options.continuous
im = Image.open(args[0]).convert("L")
pixels = im.load()
segments = max(20,im.size[0])
bottom = bottomLayers * layerHeight
abp = options.abp

init()
makeShape()
