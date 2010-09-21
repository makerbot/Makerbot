
from optparse import OptionParser
from Gerber import Gerber

def main():
    usage = "usage: %prog [options] filename > output.gcode"
    
    parser = OptionParser(usage)
    parser.add_option("--feedrate", dest="feed_rate", default=700,
                      help="x and y feedrate")
    parser.add_option("--servoup", dest="servo_up", default=40,
                      help="servo's up position")
    parser.add_option("--servodown", dest="servo_down", default=30,
                      help="servo's down position")
    parser.add_option("--linewidth", dest = "line_width", default=0.02,
                      help="line width of pen")
    parser.add_option("--startdelay", dest = "start_delay", default=50,
                      help="delay after putting pen down")
    parser.add_option("--stopdelay", dest = "stop_delay", default=150,
                      help="delay after bringing pen up")
    
    (options, args) = parser.parse_args()
    
    if len(args) < 1:
        parser.error("incorrect number of arguments")
        
    try:
        gerber_file = open( args[0] )
    except:
        print "Could not open file" 
        return 
    
    
    gerber = Gerber(gerber_file, float(options.feed_rate), 
                    float(options.servo_up), float(options.servo_down), 
                    float(options.line_width), float(options.start_delay), 
                    float(options.stop_delay))
    gerber.parse_file(None)
    gerber.output_GCODE()
    
    if(gerber_file != None):
        gerber_file.close()
                            
if __name__=='__main__':
    main()
