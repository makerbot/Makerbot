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

prefixFile= "start.gcode"
suffixFile= "end.gcode"
suffixFileABP = "end-ABP.gcode"
absoluteExtrusion = 0.0

def output(str):
    if outFile:
        if str:
            outFile.write(str+"\n")
    else:
        print output

def loadFileToString(fileName):
    f = open(fileName,"r")
    return f.read()

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
    global rBottomMm, absoluteExtrusion
    z = layerHeight * layer
    points = makeSpiralPoints(rBottomMm+extrusionWidth)
    if (layer % 2) == 0:
        points.reverse()
    for p in points:
        outStr = "G1 X%f Y%f Z%f F%f" % (p[0],p[1],z,baseFeedrate)
        if options.extrusionRate:
            absoluteExtrusion = options.extrusionRate + absoluteExtrusion
            outStr = outStr + " E%f" % (absoluteExtrusion)
        output(outStr)

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
    global absoluteExtrusion
    invvalue = 1.0-value
    feedrate = baseFeedrate * ((invvalue * maxAdjustment) + value)
    start = getXYZ(layer, segment-1)
    end = getXYZ(layer,segment)
    outStr = "G1 X%f Y%f Z%f F%f" % (end[0],end[1],end[2],feedrate)
    if options.extrusionRate:
        absoluteExtrusion = options.extrusionRate + absoluteExtrusion
        outStr = outStr + " E%f" % absoluteExtrusion
    output(outStr)

def makeShape():
    global absoluteExtrusion
    output(loadFileToString(options.prefixFile))
    output("M101")
    output("(Base)")
    for i in range(0,bottomLayers):
        makeBottom(i)
    if bottomLayers > 0:
        # add single-layer seal
        output("(Adding seal along bottom)")
        for segment in range(0, segments):
            r = rBottomMm - extrusionWidth
            angle = anglePerSegment * segment
            z = bottom + layerHeight
            x = -math.sin(angle) * r
            y = math.cos(angle) * r
            outStr = "G1 X%f Y%f Z%f F%f" % (x,y,z,baseFeedrate)
            if options.extrusionRate:
                absoluteExtrusion = options.extrusionRate + absoluteExtrusion
                outStr = outStr + " E%f" % absoluteExtrusion
    output("(Sides)")
    for layer in range(0,int(layerCount)):
        for segment in range(0, segments):
            x = segment
            y = (im.size[1] - int(float(im.size[1]*layer)/layerCount)) - 1
            output(makeSegment(layer, segment, pixels[x,y]/256.0))
    output("M103")
    if abp:
        output(loadFileToString(suffixFileABP))
    else:
        output(loadFileToString(options.suffixFile))


usage = "usage: %prog [options] image.png"
parser = OptionParser(usage = usage)
parser.add_option("-o","--output-file",type="string",dest="outputFile",
                  help="output filename (default is standard output)",default="out.gcode")
parser.add_option("-p","--prefix",type="string",dest="prefixFile",
                  help="prefix file",default=prefixFile)
parser.add_option("-s","--suffix",type="string",dest="suffixFile",
                  help="the suffix file, will be added at the end.",default=suffixFile)
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
parser.add_option("-e","--extrusion-rate",type="float",dest="extrusionRate",
                  help="set the extrusion rate, and adds E-codes")
#parser.add_option("--rexp",type="string"
(options,args) = parser.parse_args()

if len(args) != 1:
    print "Please provide exactly one filename as an argument."
    parser.print_help()
    exit()

outFile = ""
if options.outputFile:
    outFile = open(options.outputFile,"w")
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
outFile.close()
