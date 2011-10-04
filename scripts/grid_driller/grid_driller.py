#!/usr/bin/python
import argparse

def makeParser():
    parser = argparse.ArgumentParser(description='Generate a drill file for a grid of holes, with (0,0,0) at the upper-left-hand surface.')
    parser.add_argument('-x', type=float, default=80.0,
                        help='The width of the platform in mm')
    parser.add_argument('-y', type=float, default=80.0,
                        help='The depth of the platform in mm')
    parser.add_argument('-d', type=float, default=3.0,
                        help='The depth of the holes to drill in mm')
    parser.add_argument('-v', type=float, default=5.0,
                        help='The hover height in mm')
    parser.add_argument('--ft', type=float, default=500.0,
                        help='The travel feedrate')
    parser.add_argument('--fd', type=float, default=5.0,
                        help='The drill feedrate')
    parser.add_argument('-n', type=float, default=5,
                        help='The distance between hole centers')
    return parser


def gcDrillHole():
    global feed_travel, feed_drill, depth, hover
    r = "G0 Z-0.01 F{0} (Travel to surface)\n".format(feed_travel)
    r = r + "G1 Z{0} F{1} (Drill hole to depth {0})\n".format(depth,feed_drill)
    r = r + "G1 Z-0.01 F{0} (Extract drill)\n".format(feed_drill)
    r = r + "G0 Z{0} F{1} (Hover)\n".format(hover,feed_travel)
    return r


def gcMoveTo(x,y):
    global feed_travel
    return "G0 X{0} Y{1} F{2} (Go to {0},{1})\n".format(x,y,feed_travel)

def gcHoleGrid():
    global width, height, density
    x = 0.0
    y = 0.0
    r = "(Drill grid start)\n"
    while x <= width:
        while y <= height:
            r = r + gcMoveTo(x,y)
            r = r + gcDrillHole()
            y = y + density
        x = x + density
        y = 0.0
    return r

parser = makeParser()
arguments = parser.parse_args()
width = arguments.x
height = arguments.y
depth = arguments.d
hover = arguments.v
feed_travel = arguments.ft
feed_drill = arguments.fd
density = arguments.n
print gcHoleGrid()
