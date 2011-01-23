from string import Template

defaultStartCode = '''\
(begin of startup)
G21 (set units to mm)
G90 (set positioning to absolute)
M108 R1.8 (set extruder speed to maximum)
M104 S230 T0 (set extruder temperature)
M109 S125 T0 (set heated-build-platform temperature)
(**** end initilization commands ****)
(**** begin homing ****)
G162 Z F500 (home Z axis maximum)
G161 X Y F2500 (home XY axes minimum)
G92 Z116.4 ( ---=== Set Z axis maximum ===--- )
G92 X-57.5 Y-57 (set zero for X and Y)
(**** end homing ****)
(**** begin pre-wipe commands ****)
M103 (Make sure extruder is off)
G1 X52.0 Y-57.0 Z10.0 F3300.0 (move to waiting position)
M6 T0 (wait for toolhead parts, nozzle, HBP, etc., to reach temperature)
(**** end pre-wipe commands ****)
M105 (get extruder temperature)
G1 X0 Y0 Z10.0 F3300.0 (move to a safe starting position)
(end of startup)
'''

defaultShutdownCode = '''\
(begin of shutdown)
M104 S0 T0 (shut off extruder)
M109 S0 T0 (shut off heated-build-platform)
G1 X0 Y0 Z20.0 F3300.0 (move to a safe ending position)
(end of shutdown)
'''

engageTool = '''\
G1 Z0.0 (head down)
M101 (extruder on)
'''

disengageTool = '''\
G1 Z5.0 (head down)
M103 (extruder off)
'''

moveXYPointTemplate = Template('G1 X$xpos Y$ypos F$speed (move to point)\n')

class ToolpathGenerator:
	""" simple state machine for a gcode generator """
	def __init__(self):
		self.xPos = 0		# Assume we start at 0,0,10. This is set in startup
		self.yPos = 0
		self.zPos = 10
		
	def open(self, filename, startcode=""):
		if (startcode==""):
			startcode = defaultStartCode
		self.filename = filename
		self.output = open(self.filename, 'w')
		self.output.write(startcode)
		
	def close(self, shutdowncode=""):
		if (shutdowncode==""):
			shutdowncode = defaultShutdownCode
		self.output.write(shutdowncode)
		self.output.close()
	
	def moveToXY(self, X, Y, S):		
		self.output.write(moveXYPointTemplate.substitute(xpos=X, ypos=Y, speed=S))
		
	def engageTool(self):
		self.output.write(engageTool)

	def disengageTool(self):
		self.output.write(disengageTool)
		
	def write(self, command):
		self.output.write(command)
		

def makeXYZigZag(generator, startX, startY, lenX, lenY, speed, Zags):
	x = startX
	y = startY
	generator.moveToXY(x,y,speed)
	generator.engageTool()
	
	for i in range(Zags):
		# move +y on even counts, -y on odd counts
		if (i % 2 == 0):
			y += lenY
		else:
			y -= lenY

		generator.moveToXY(x,y,speed)
		
		# if this isn't the last motion, then move +x
		if (i + 1 != Zags):
			x += lenX
			generator.moveToXY(x,y,speed)
	
	generator.disengageTool()