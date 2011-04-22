#!/usr/bin/python

from toolpathgenerator import *

startCode = '''\
(*** Tool Path Generator ***)
G21 (set units to mm)
G90 (set positioning to absolute)
M103 (Make sure extruder is off)
(**** begin homing ****)
G162 Z F500 (home Z axis maximum)
G161 X Y F2500 (home XY axes minimum)
M132 X Y Z A B (Recall stored home offsets for XYZAB axis)
'''
	
gen = ToolpathGenerator()
gen.open('platform_leveler.gcode', startcode=startCode)
gen.moveToXYZ(0,0,20,1500)

for x in range(-40,41,40):
	for y in range(-50,51,50):
		gen.moveToXYZ(x,y,10,1500)
		gen.moveToXYZ(x,y,0,1500)
		gen.prompt("Ok.")
		gen.moveToXYZ(x,y,10,1500)

gen.close(shutdowncode="")
