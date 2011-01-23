from toolpathgenerator import *
from string import Template

startCode = '''\
(begin of startup)
G21 (set units to mm)
G90 (set positioning to absolute)
M104 S225 T0 (set extruder temperature)
(**** end initilization commands ****)
(**** begin pre-wipe commands ****)
M6 T0 (wait for toolhead parts, nozzle, HBP, etc., to reach temperature)
M105 (get extruder temperature)
(end of startup)
'''

shutdownCode = '''\
(begin of shutdown)
M104 S0 T0 (shut off extruder)
(end of shutdown)
'''

rpmTemplate = Template('M108 R$rpm\n')
dwellTemplate = Template('G4 P$time\n')


shakeRPM = 5
shakePeriod = 200
shakeCount = 1000

gen = ToolpathGenerator()
gen.open('shake_test.gcode', startCode)

# do a bunch of different kinds of shaking
for shakePeriod in range(100,1000,100):
	for shakeRPM in range(3,8):
		# Extrude at a normal speed for a bit to clear the pipeline
		gen.write(rpmTemplate.substitute(rpm=1.8))
		gen.write("M101\n")
		gen.write(dwellTemplate.substitute(time=10000))
		gen.write("M102\n")
		
		gen.write("(Running test: period=" + str(shakePeriod) + ", rpm=" + str(shakeRPM) + ")\n")
		gen.write(rpmTemplate.substitute(rpm=shakeRPM))
		
		# Then do the shake
		for i in range(0, shakeCount):
			gen.write("M101\n")
			gen.write(dwellTemplate.substitute(time=shakePeriod/2))
			gen.write("M102\n")
			gen.write(dwellTemplate.substitute(time=shakePeriod/2))

gen.write("M103\n")
gen.close(shutdownCode)