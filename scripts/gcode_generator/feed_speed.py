from toolpathgenerator import *
	
gen = ToolpathGenerator()
gen.open('zigzag.gcode')
makeXYZigZag(gen, -30, -30, 2, 60, 300, 5)
makeXYZigZag(gen, -15, -30, 2, 60, 600, 5)
makeXYZigZag(gen, 0, -30, 2, 60, 1200, 5)
gen.write("M108 R2.5\n");
makeXYZigZag(gen, 15, -30, 2, 60, 600, 5)
makeXYZigZag(gen, 30, -30, 2, 60, 1200, 5)
gen.close()