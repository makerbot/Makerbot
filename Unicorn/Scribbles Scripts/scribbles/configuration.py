#
# This file contains the default configuration for the
# DXF->GCode converter.
#


# The G code preamble.  These codes are emitted before anything else
# is written.  Each G code should be a seperate string.
preamble = ["G90","G17"]

# The G code postscript.  These codes are emitted when the build is done.
# Each G code should be a seperate string.
postscript = ["(end of print job)", "M107", "M126", "M18", "M127", "G18"]

# An array containing the G codes to emit to start the frostruder.
# Each G code should be a seperate string.
start_codes = []

# An array containing the G codes to emit to stop the frostruder.
# Each G code should be a seperate string.
stop_codes = []

# The rate at which to draw while extruding, in mm per minute.
draw_rate = 1500.0 #1000.0

# The rate at which to move when not extruding, in mm per minute.
travel_rate = 250.0
