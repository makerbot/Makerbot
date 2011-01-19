from toolpathgenerator import *
from string import Template

rpmTemplate = Template('M108 R$rpm\n')
dwellTemplate = Template('G4 P$time\n')


shakeRPM = 5
shakePeriod = 200
shakeCount = 500

gen = ToolpathGenerator()
gen.open('shake_test.gcode')
gen.write(rpmTemplate.substitute(rpm=shakeRPM))

for i in range(0, shakeCount):
	gen.write("M101\n")
	gen.write(dwellTemplate.substitute(time=shakePeriod/2))
	gen.write("M102\n")
	gen.write(dwellTemplate.substitute(time=shakePeriod/2))

gen.write("M103\n")
gen.close()