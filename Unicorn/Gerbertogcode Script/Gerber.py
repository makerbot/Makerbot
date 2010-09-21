import re
import math
from GerberConstants import GerberConstants

        
###################################
#
###################################  

class GerberLayerPolarity():
    def __init__(self):
        self.layer_polarity = None 

        
###################################
#
###################################  

class GerberImagePolarity():
    def __init__(self):
        self.image_polarity = None 
         
###################################
#
###################################  
       
class GerberApatureDefintion():
    def __init__(self):
        self.d_code = None
        self.X_dim  = None
        self.X_hole_dim = None
        self.Y_dim  = None
        self.Y_hole_dim = None 
        self.macro = None
        self.apature_type = None 
        self.outside_diameter = None
        self.side_count = None
         
###################################
#
###################################  
class GerberApatureCircle():
    def __init__(self):
        self.exposure = None
        self.diameter = None
        self.x_center = None
        self.y_center = None
        
        
###################################
#
###################################  

class GerberApatureLine():
    def __init__(self):
        self.exposure = None
        self.line_width = None
        self.x_start = None
        self.y_start = None
        self.x_end = None
        self.y_end = None
        self.width = None
        self.height = None
        self.x_center = None
        self.y_center = None
        self.rotation = None 
        
###################################
#
###################################  

class GerberApatureOutline():
    def __init__(self):
        self.exposure = None
        self.point_count = None
        self.x_start = None
        self.y_start = None
        self.points = []
        self.rotation = None
    
##################################
#
##################################
class GerberPoint():
    def __init__(self):
        self.x = None
        self.y = None 
###################################
#
###################################  

class GerberApaturePolygon():
    def __init__(self):
        self.vertice_count = None
        self.x_center = None
        self.y_center = None
        self.diameter = None
        self.rotation = None
        
###################################
#
###################################  

class GerberApatureMorie():
    def __init__(self):
        self.x_center = None
        self.y_center = None
        self.outside_diameter = None
        self.line_thickness = None 
        self.gap_thickness = None
        self.number_of_circles = None
        self.cross_hair_thickness = None
        self.cross_hair_length = None
        self.rotation = None
###################################
#
###################################  

class GerberApatureThermal():
    def __init__(self):
        self.x_center = None
        self.y_center = None
        self.outside_diameter = None
        self.inside_diameter = None
        self.cross_hair_thickness = None
        self.rotation = None
        

###################################
#
###################################  
       
class GerberApatureBlock(): 
    def __init__(self): 
        self.block_type = None
        self.data = None
     
###################################
#
###################################  
 
class GerberApatureMacro():
    def __init__(self):
        self.am_name = None 
        self.am_blocks = [] 
        
###################################
#
################################### 
       
class GerberAxisSelectCommand():
    def __init__(self):
        self.A = None 
        self.B = None

###################################
#
###################################  

class GerberFormatStatementCommand():
    def __init__(self):
        self.coordinate_format_x = None
        self.coordinate_format_y = None
        self.zero_omission = None
        self.coordinate_notation = None
        self.sequence_number = None
        self.general_code_length = None
        self.draft_code_length = None
        self.misc_code_length = None
        
###################################
#
###################################  
       
class GerberGeneralCommand(): 
    def __init__(self):
        self.general_type = None
###################################
#
###################################  

class GerberMachineCommand(): 
    def __init__(self):
        self.machine_type = None
        
###################################
#
###################################  
class GerberMoveCommand():
    
    ###################################
    #
    ###################################  
    def __init__(self):
        self.x = None
        self.y = None
        self.z = None
        self.i = None 
        self.j = None 
        self.d = None 
        
###################################
#
################################### 
class GerberDraftCommand():
    
    ###################################
    #
    ###################################
    def __init__(self):
        self.draft_type = None
        

###################################
#
###################################  
class GerberCommand():
   
    ###################################
    #
    ###################################  
    def __init__(self, command_type):
        self.command_type = command_type
        self.command = None
        
   ###################################
   #
   ###################################       
    def set_command(command):
        self.command = command
     

    
###################################
#
###################################        
class Gerber():
    
    x_re = re.compile(r"X([0-9]+)")
    y_re = re.compile(r"Y([0-9]+)")
    d_re = re.compile(r"D([0-9]+)")
    m_re = re.compile(r"M([0-9]+)")
   
       
    ###################################
    #
    ###################################

    def __init__(self, file, feed_rate, servo_up, servo_down, line_width, start_delay, stop_delay):
        self.file = file
         
        self.format_statement_command = None  
        self.image_rotation_command = None 
        self.axis_select_command = None 
        self.layer_polarity = None
        self.image_polarity = None 
        
        self.feed_rate = str(feed_rate)
        self.line_width = line_width
        self.servo_up = servo_up
        self.servo_down = servo_down
        self.start_delay = start_delay
        self.stop_delay = stop_delay
     
        self.gerber_commands = [] 
        self.apature_definitions = {}
        self.apature_macros = {} 
 
    ###################################
    #
    ###################################

    def create_RE(self,letter):
        regex = '%s([0-9]+)' % letter
        return re.compile(regex)
 
    ###################################
    #
    ###################################
    def find_value(self, command, letter):
      
        regex = self.create_RE(letter) 
        
        match = regex.search( command )
        
        if( match ):
            return match.group(1)
        else:
            return None
         
    ###################################
    #
    ###################################

    def remove_zeros(self, segment, leading):
        stripped = ""

        if leading:
            stripped = segment.lstrip(' 0')
        else :
            stripped = segment.rstrip(' 0')

        if len(stripped) == 0:
            stripped = "0"

        return stripped
    
    
    ###################################
    #
    ###################################

    def parse_file(self):
        self.parse_file(None)
         
    ###################################
    #
    ###################################

    def parse_file(self, file):
        
        multiline = False 
        previous_line = ""
        
        if( file != None ):
            self.file = file 
           
        if( self.file != None):
            
            for line in self.file:
                command_line = line.strip() 
               
                if( len( command_line ) == 0 ):
                    continue
           
                if( multiline == False ):
                    previous_line = command_line
                else:
                    previous_line += command_line
                    command_line = previous_line 
                
                command_type = command_line[0]
                command_data = command_line[1:]
                parsed_gerber_commands = []
                
                if( command_type == GerberConstants.g_code ):
                    parsed_gerber_commands = self.parse_general( self.split_commands( command_data ) )
                 
                if( command_type == GerberConstants.p_code ): 
                    
                    if( command_line[ len( command_line ) -1] == GerberConstants.p_code ):
                        multiline = False
                        command_data = command_line.strip("%")
                       
                        ###
                        # Macros require different parsing than normal multiline Gerber commands 
                        # BUG: This will break if a macro is embedded inside of another parameter 
                        #       multiline command ex. %LF*%*%AM*%  I'm not sure that is even valid
                        #       according to the spec. 
                        
                        if( len( command_data ) > 3 ):
                            if( command_data[ 0:2 ] == GerberConstants.p_apature_macro ):
                                self.parse_macros( command_data ) 
                            else: 
                                parsed_gerber_commands = self.parse_parameter( self.split_commands( command_data ) )
                    else:
                        multiline = True
                        continue
                    
                if( command_type == GerberConstants.m_code ):
                    parsed_gerber_commands = self.parse_machine( self.split_commands( command_data ) )
                    
                if( command_type == GerberConstants.d_code ):
                    parsed_gerber_commands = self.parse_draft( self.split_commands( command_data ) )
                    
                if( command_type == GerberConstants.x_code or 
                    command_type == GerberConstants.y_code ):
                    parsed_gerber_commands = self.parse_coord( self.split_commands(line) )
                    
                if(parsed_gerber_commands != None): 
                    for parsed_gerber_command in parsed_gerber_commands:
                        self.gerber_commands.append(parsed_gerber_command)
                    
   
    ###################################
    #
    ###################################
    def split_commands(self, line):
        
        cleaned_commands = []
        commands = line.split(GerberConstants.command_end)
        
        for command in commands:
            command.strip()
            if(len(command) != 0):
                cleaned_commands.append(command)
                
        return cleaned_commands 
    
                     
    ###################################
    #
    ###################################

    def parse_parameter( self, commands ):
        
        gerber_commands = []
        
        for command in commands:
            
            if( len(command) < 3):
                continue
            
            gerber_command = GerberCommand("p")
            command_type = command[0:2]
            command_data = command[2:]
           
            
            if( command_type == GerberConstants.p_apature_definition ):
                
                self.apature_def = GerberApatureDefintion()
                self.apature_def.d_code = self.find_value( command, "D" )
                
                ad_command = command.split( ',' )
                
                if( len( ad_command ) == 1 ):
                    return 
                
                self.apature_def.apature_type =  ad_command[0][len( ad_command[0] ) - 1] 
                
                apature_mods = ad_command[1].split( 'X' )
               
                mod_count = len(apature_mods)
                
                if(self.apature_def.apature_type == GerberConstants.ad_circle):
                    
                    if(mod_count >= 1):
                        self.apature_def.outside_diameter = apature_mods[0]
                        
                    if(mod_count >= 2): 
                        self.apature_def.X_hole_dim = apature_mods[1]
                        
                    if(mod_count >= 3):
                        self.apature_def.Y_hole_dim = apature_mods[2] 
                        
                    
                if(self.apature_def.apature_type == GerberConstants.ad_rectangle):
                     
                    if(mod_count >= 1):
                        self.apature_def.X_dim = apature_mods[0]
                        
                    if(mod_count >= 2): 
                        self.apature_def.Y_dim = apature_mods[1]
                        
                    if(mod_count >= 3):
                        self.apature_def.X_hole_dim = apature_mods[2] 
                    
                    if(mod_count >= 4):
                        self.apature_def.Y_hole_dim = apature_mods[3] 
                        
                        
                if(self.apature_def.apature_type == GerberConstants.ad_oval):
                     
                    if(mod_count >= 1): 
                        self.apature_def.X_dim = apature_mods[0]
                        
                    if(mod_count >= 2):
                        self.apature_def.Y_dim = apature_mods[1] 
 
                    if(mod_count >= 3):
                        self.apature_def.X_hole_dim = apature_mods[2] 
 
                    if(mod_count >= 4):
                        self.apature_def.Y_hole_dim = apature_mods[3] 
                        
                if(self.apature_def.apature_type == GerberConstants.ad_polygon):
                       
                    if(mod_count >= 1): 
                        self.apature_def.outside_diameter = apature_mods[0]
                        
                    if(mod_count >= 2):
                        self.apature_def.side_count =  apature_mods[1] 
 
                    if(mod_count >= 3):
                        self.apature_def.X_degrees = apature_mods[2] 
 
                    if(mod_count >= 4):
                        self.apature_def.X_hole_dim = apature_mods[3] 
                        
                    if(mod_count >= 5):
                        self.apature_def.Y_hole_dim = apature_mods[4] 
                        
                self.apature_definitions[self.apature_def.d_code] =  self.apature_def
                #self.apature_def.macro = self.apature_macros[ the macro name goes here ]
 
                
            if( command_type == GerberConstants.p_layer_polarity ):
                self.layer_polarity = GerberLayerPolarity();
                self.layer_polarity.layer_polarity = command_data 
                
            if( command_type == GerberConstants.p_image_polarity ): 
                self.image_polarity = GerberImagePolarity() 
                self.image_polarity.image_polarity = command_data
                
            if( command_type == GerberConstants.p_format_statement ):
                
                self.format_statement_command = GerberFormatStatementCommand()
                self.format_statement_command.coordinate_format_x = self.find_value(command, "X") 
                self.format_statement_command.coordinate_format_y = self.find_value(command, "Y") 
                self.format_statement_command.draft_code_length   = self.find_value(command, "D")
                self.format_statement_command.general_code_length = self.find_value(command, "G")
                self.format_statement_command.misc_code_length    = self.find_value(command, "M")
                self.format_statement_command.sequence_number     = self.find_value(command, "N")
                
                if( command.find(GerberConstants.fs_omit_leading_zeros) != -1 ): 
                    self.format_statement_command.zero_omission = GerberConstants.fs_omit_leading_zeros 
                    
                if( command.find(GerberConstants.fs_omit_trailing_zeros) != -1 ): 
                    self.format_statement_command.zero_omission = GerberConstants.fs_omit_trailing_zeros
                   
                if( command.find(GerberConstants.fs_absolute_coords) != -1 ):
                    self.format_statement_command.coordinate_notation = GerberConstants.fs_absolute_coords
                    
                if( command.find(GerberConstants.fs_incremental_coords) != -1 ):
                    self.format_statement_command.coordinate_notation = GerberConstants.fs_incremental_coords
                
                
            gerber_commands.append(gerber_command)
        return gerber_commands
                 
   
    ########################
    #
    ########################
    def parse_macros(self, command_data):
        
        ################## 
        # The macros come before the ADs in the gerber files
        # Below we're going to build up a hash tables of macro names to macro objects
        # then we'll do a look up in the table and assigne the macro object as needed
        # for output For each of the ADs 
        # Well have to make a macro -> tool path conversion utility for output
        # because macros can be dynamic each of these will have to be evaluated at output time 
        # yar 
        ##################
    
        macro = GerberApatureMacro()
        
        split_macro = self.split_commands( command_data )

        macro_header = split_macro[0] 
     
        if( len(macro_header) > 2 ):
            macro.am_name = macro_header[2:]
        
        macro_blocks = split_macro[1:]
    
        for macro_block in macro_blocks:
            
            macro_part = GerberApatureBlock()
            macro_parts = macro_block.split(',')
            macro_type = macro_parts[0]
            
            macro_data = None
            
            macro_part.block_type = macro_type
            
            if( macro_type == GerberConstants.am_circle):
                macro_data = GerberApatureCircle()
                macro_data.exposure = macro_parts[1]
                macro_data.diameter = macro_parts[2] 
                macro_data.x_center = macro_parts[3]
                macro_data.y_center = macro_parts[4]
                
            if( macro_type == GerberConstants.am_line_vector_alt or
                macro_type == GerberConstants.am_line_vector ):
                macro_data = GerberApatureLine()
                macro_data.exposure = macro_parts[1]
                macro_data.line_width = macro_parts[2]
                macro_data.x_start = macro_parts[3]
                macro_data.y_start = macro_parts[4]
                macro_data.x_end = macro_parts[5]
                macro_data.y_end = macro_parts[6]
                macro_data.rotation = macro_parts[7]
                
            if( macro_type == GerberConstants.am_line_center ):
                macro_data = GerberApatureLine()
                macro_data.exposure = macro_parts[1]
                macro_data.width = macro_parts[2]
                macro_data.height = macro_parts[3]
                macro_data.x_center = macro_parts[4]
                macro_data.y_center = macro_parts[5]
                macro_data.rotation = macro_parts[6]
                
           
            if( macro_type == GerberConstants.am_line_lower_left ): 
                macro_data = GerberApatureLine()
                macro_data.exposure = macro_parts[1]
                macro_data.width = macro_parts[2]
                macro_data.height = macro_parts[3]
                macro_data.x_start = macro_parts[4]
                macro_data.y_start = macro_parts[5]
                macro_data.rotation = macro_parts[6]
                
            if( macro_type == GerberConstants.am_outline ): 
                macro_data = GerberApatureOutline()
                macro_data.point_count = macro_parts[1]
               #TODO: finish parsing points to array  
                
            if( macro_type == GerberConstants.am_polygon ): 
                macro_data = GerberApaturePolygon() 
                macro_data.exposure = macro_parts[1] 
                macro_data.vertice_count = macro_parts[2]
                macro_data.x_center = macro_parts[3]
                macro_data.y_center = macro_parts[4]
                macro_data.diameter = macro_parts[5]
                macro_data.rotation = macro_parts[6]
                
            if( macro_type == GerberConstants.am_morie ): 
                macro_data = GerberApatureMorie()
                macro_data.x_center = macro_parts[1]
                macro_data.y_center = macro_parts[2]
                macro_data.outside_diameter = macro_parts[3]
                macro_data.inside_diameter = macro_parts[4]
                macro_data.gap_thickness = macro_parts[5]
                macro_data.number_of_circles = macro_parts[6]
                macro_data.cross_hair_thickness = macro_parts[7]
                macro_data.cross_hair_length = macro_parts[8] 
                macro_data.rotation = macro_parts[9] 
                
            if( macro_type == GerberConstants.am_thermal ): 
                macro_data = GerberApatureThermal()
                macro_data.x_center = macro_parts[1]
                macro_data.y_center = macro_parts[2]
                macro_data.outside_diameter = macro_parts[3]
                macro_data.inside_diameter = macro_parts[4]
                macro_data.cross_hair_thickness = macro_parts[5]
                macro_data.rotation = macro_parts[6] 
                
            macro_part.data = macro_data 
            macro.am_blocks.append(macro_part)
           
        ## add the macro 
        self.apature_macros[macro.am_name] = macro
          
            
    ###################################
    #
    ###################################

    def parse_general(self, commands):
        
        gerber_commands = []
        gerber_command = GerberCommand("g")
        general_command = GerberGeneralCommand()
        

        for command in commands:
            general_command.general_type = command
            gerber_command.command = general_command
            gerber_commands.append(gerber_command)
            
        return gerber_commands

         
    ###################################
    #
    ###################################

    def parse_draft(self, commands):
        gerber_commands = [] 
        for command in commands:
            gerber_command = GerberCommand("d")
            gerber_command.command = GerberDraftCommand()
            gerber_command.command.draft_type = command
            gerber_commands.append(gerber_command)

        return gerber_commands
  
    ###################################
    #
    ###################################

    def parse_machine(self, commands):
        gerber_commands = []
        for command in commands:
            gerber_command = GerberCommand("m")
            gerber_command.command = GerberMachineCommand()
            gerber_command.command.machine_type = command
            gerber_commands.append(gerber_command)

        return gerber_commands
    
    
    ###################################
    #
    ###################################

    def parse_coord(self, commands):
        gerber_commands = []
        for command in commands:
            
            move = GerberMoveCommand()
            move.x = self.find_value(command, "X") 
            move.y = self.find_value(command, "Y") 
            move.d = self.find_value(command, "D")
            
            if( self.format_statement_command != None ):
                
                if( self.format_statement_command.coordinate_format_x != None and 
                   move.x != None ): 
                    
                    leading_x = move.x[ 0 : int(self.format_statement_command.coordinate_format_x[0])]
                    trailing_x = move.x[ int(self.format_statement_command.coordinate_format_x[0]):]
                    
                    if( self.format_statement_command.zero_omission == GerberConstants.fs_omit_leading_zeros ):
                        leading_x = self.remove_zeros(leading_x, True)
                        
                    if ( self.format_statement_command.zero_omission == GerberConstants.fs_omit_trailing_zeros ):
                        self.remove_zeros(trailing_x, False)                   
                        
                    move.x = leading_x + "." + trailing_x

                if(self.format_statement_command.coordinate_format_y != None and
                   move.y != None): 

                    leading_y = move.y[ 0 : int(self.format_statement_command.coordinate_format_y[0])]
                    trailing_y = move.y[ int(self.format_statement_command.coordinate_format_y[0]):]

                    if (self.format_statement_command.zero_omission == GerberConstants.fs_omit_leading_zeros):
                        leading_y = self.remove_zeros(leading_y, True)

                    if (self.format_statement_command.zero_omission == GerberConstants.fs_omit_trailing_zeros):
                        trailing_y = self.remove_zeros(trailing_y, False)

                    move.y = leading_y + "." + trailing_y
            
            gerber_command = GerberCommand("c")
            gerber_command.command = move 
            gerber_commands.append(gerber_command)
           
        return gerber_commands
    
    ##########################
    #
    ##########################
    def output_rectangle_GCODE(self, x_pos, y_pos, x_dim, y_dim, x_hole_dim, y_hole_dim):
        
        if ( x_dim != None and y_dim != None ):
            print "(valid rectangle)"
            rectangle_current_x = (x_pos) + (float(x_dim)/2)
            rectangle_current_y = (y_pos) - (float(y_dim)/2)
            print "M300 S%d (pen up)" %self.servo_up
            print "G4 P%d" %self.stop_delay 
            print "G1 X" + str(rectangle_current_x) + " Y" + str(rectangle_current_y) + " F" + self.feed_rate
            rectangle_current_y += float(y_dim)
            print "M300 S%d (pen down)" %self.servo_down
            print "G4 P%d" %self.start_delay 
            print "G1 X" + str(rectangle_current_x) + " Y" + str(rectangle_current_y) + " F" + self.feed_rate
            rectangle_current_x -= float(x_dim)
            print "G1 X" + str(rectangle_current_x) + " Y" + str(rectangle_current_y) + " F" + self.feed_rate
            rectangle_current_y -= float(y_dim)
            print "G1 X" + str(rectangle_current_x) + " Y" + str(rectangle_current_y) + " F" + self.feed_rate
            rectangle_current_x += float(x_dim)
            print "G1 X" + str(rectangle_current_x) + " Y" + str(rectangle_current_y) + " F" + self.feed_rate
            
            #return to center
            print "M300 S%d (pen up)" %self.servo_up
            print "G4 P%d" %self.stop_delay 
            print "G1 X" + str(x_pos) + " Y" + str(y_pos) + " F" + self.feed_rate
            
        self.output_hole_GCODE(x_pos, y_pos, x_hole_dim, y_hole_dim)
                
    #############################
    #
    #############################
    
    def output_circle_GCODE(self, x_pos, y_pos, outer_diameter, x_hole_dim, y_hole_dim) :
        
        if (outer_diameter != None) :
            #valid circle
            circle_current_x = x_pos - (float(outer_diameter)/2)
            circle_current_y = y_pos
            
            print "M300 S%d (pen up)" %self.servo_up
            print "G4 P%d" %self.stop_delay
            print "G1 X" + str(circle_current_x) + " Y" + str(circle_current_y) + " F" + self.feed_rate
            
            print "M300 S%d (pen down)" %self.servo_down
            print "G4 P%d" %self.start_delay 
            print "G3 I" + str(float(outer_diameter)/2) + "J0 F" + self.feed_rate
            
            #return to center
            print "M300 S%d (pen up)" %self.servo_up
            print "G4 P%d" %self.stop_delay 
            print "G1 X" + str(x_pos) + " Y" + str(y_pos) + " F" + self.feed_rate
            
        self.output_hole_GCODE(x_pos, y_pos, x_hole_dim, y_hole_dim)
            
   
    #############################
    #
    #############################
    
    def output_oval_GCODE(self, x_pos, y_pos, x_dim, y_dim, x_hole_dim, y_hole_dim) :
        
        if (x_dim != None and y_dim != None) :
            #check if horizontal or vertical
            if x_dim >= y_dim :
                #horizontal
                oval_current_x = x_pos + (float(x_dim)-float(y_dim))/2
                oval_current_y = y_pos - float(y_dim)/2
                oval_arc_center_x = 0
                oval_arc_center_y = float(y_dim)/2
                
                print "M300 S%d (pen up)" %self.servo_up
                print "G4 P%d" %self.stop_delay 
                print "G1 X" + str(oval_current_x) + " Y" + str(oval_current_y) + " F" + self.feed_rate
                
                print "M300 S%d (pen down)" %self.servo_down
                print "G4 P%d" %self.start_delay 
                oval_current_y += float(y_dim)
                print ("G3 X" + str(oval_current_x) + " Y" + str(oval_current_y) + " I" 
                       + str(oval_arc_center_x) + " J" + str(oval_arc_center_y) + " F" + self.feed_rate)
                oval_current_x -= (float(x_dim)-float(y_dim))
                print "G1 X" + str(oval_current_x) + " Y" + str(oval_current_y) + " F" + self.feed_rate
                oval_current_y -= float(y_dim)
                oval_arc_center_x = 0
                oval_arc_center_y = -float(y_dim)/2
                print ("G3 X" + str(oval_current_x) + " Y" + str(oval_current_y) + " I" 
                       + str(oval_arc_center_x) + " J" + str(oval_arc_center_y) + " F" + self.feed_rate)
                oval_current_x += (float(x_dim)-float(y_dim))
                print "G1 X" + str(oval_current_x) + " Y" + str(oval_current_y) + " F" + self.feed_rate
            
                #return to center
                print "M300 S%d (pen up)" %self.servo_up
                print "G4 P%d" %self.stop_delay 
                print "G1 X" + str(x_pos) + " Y" + str(y_pos) + " F" + self.feed_rate
            
            
            else:
                #vertical
                oval_current_x = x_pos + float(x_dim)/2
                oval_current_y = y_pos + (float(y_dim)-float(x_dim))/2
                oval_arc_center_x = -float(x_dim)/2
                oval_arc_center_y = 0
                
                print "M300 S%d (pen up)" %self.servo_up
                print "G4 P%d" %self.stop_delay 
                print "G1 X" + str(oval_current_x) + " Y" + str(oval_current_y) + " F" + self.feed_rate
                
                print "M300 S%d (pen down)" %self.servo_down
                print "G4 P%d" %self.start_delay 
                oval_current_x -= float(x_dim)
                print ("G3 X" + str(oval_current_x) + " Y" + str(oval_current_y) + " I" 
                       + str(oval_arc_center_x) + " J" + str(oval_arc_center_y) + " F" + self.feed_rate)
                oval_current_y -= (float(y_dim)-float(x_dim))
                print "G1 X" + str(oval_current_x) + " Y" + str(oval_current_y) + " F" + self.feed_rate
                oval_current_x += float(x_dim)
                oval_arc_center_x = float(x_dim)/2
                oval_arc_center_y = 0
                print ("G3 X" + str(oval_current_x) + " Y" + str(oval_current_y) + " I" 
                       + str(oval_arc_center_x) + " J" + str(oval_arc_center_y) + " F" + self.feed_rate)
                oval_current_y += (float(y_dim)-float(x_dim))
                print "G1 X" + str(oval_current_x) + " Y" + str(oval_current_y) + " F" + self.feed_rate
                
                #return to center
                print "M300 S%d (pen up)" %self.servo_up
                print "G4 P%d" %self.stop_delay 
                print "G1 X" + str(x_pos) + " Y" + str(y_pos) + " F" + self.feed_rate
                
            
            self.output_hole_GCODE(x_pos, y_pos, x_hole_dim, y_hole_dim)
             
    #################################
    #
    ################################
    def output_polygon_GCODE(self, x_pos, y_pos, vertices, diameter, rotation) :
        theta = math.radians(360/float(vertices))
        phi = math.radians(float(rotation))
        poly_current_x = x_pos + math.cos(phi)*diameter/2
        poly_current_y = y_pos + math.sin(phi)*diameter/2
        
        print "M300 S%d (pen up)" %self.servo_up
        print "G4 P%d" %self.stop_delay 
        print "G1 X" + str(poly_current_x) + " Y" + str(poly_current_y) + " F" + self.feed_rate
        
        i = 1
        while (i <= vertices):
            poly_current_x = x_pos + math.cos(phi+theta*i)*diameter/2
            poly_current_y = y_pos + math.sin(phi+theta*i)*diameter/2
            print "M300 S%d (pen down)" %self.servo_down
            print "G4 P%d" %self.start_delay 
            print "G1 X" + str(poly_current_x) + " Y" + str(poly_current_y) + " F" + self.feed_rate
            i += 1
                
                
    def output_hole_GCODE(self, x_pos, y_pos, x_hole_dim, y_hole_dim) :
        
            if (x_hole_dim != None and y_hole_dim == None) :
                #circular hole
                hole_current_x = x_pos - (float(x_hole_dim)/2)
                hole_current_y = y_pos
                
                print "M300 S%d (pen up)" %self.servo_up
                print "G4 P%d" %self.stop_delay 
                print "G1 X" + str(circle_current_x) + " Y" + str(circle_current_y) + " F" + self.feed_rate
                print "M300 S%d (pen down)" %self.servo_down
                print "G4 P%d" %self.start_delay 
                print "G3 I" + str(float(x_hole_dim)/2) + "J0 F" + self.feed_rate
            
                #return to center
                print "M300 S%d (pen up)" %self.servo_up
                print "G4 P%d" %self.stop_delay 
                print "G1 X" + str(x_pos) + " Y" + str(y_pos) + " F" + self.feed_rate
                
            elif (x_hole_dim != None and y_hole_dim != None) :
                #rectangular/square hole
                hole_current_x = (x_pos) + (float(x_hole_dim)/2)
                hole_current_y = (y_pos) - (float(y_hole_dim)/2)
                print "M300 S%d (pen up)" %self.servo_up
                print "G4 P%d" %self.stop_delay 
                print "G1 X" + str(hole_current_x_current_x) + " Y" + str(hole_current_y) + " F" + self.feed_rate
                
                rectangle_current_y += float(y_hole_dim)
                
                print "M300 S%d (pen down)" %self.servo_down
                print "G4 P%d" %self.start_delay 
                print "G1 X" + str(hole_current_x) + " Y" + str(hole_current_y) + " F" + self.feed_rate
                rectangle_current_x -= float(x_hole_dim)
                print "G1 X" + str(hole_current_x) + " Y" + str(hole_current_y) + " F" + self.feed_rate
                rectangle_current_y -= float(y_hole_dim)
                print "G1 X" + str(hole_current_x) + " Y" + str(hole_current_y) + " F" + self.feed_rate
                rectangle_current_x += float(x_hole_dim)
                print "G1 X" + str(hole_current_x) + " Y" + str(hole_current_y) + " F" + self.feed_rate
                
                #return to center
                print "M300 S%d (pen up)" %self.servo_up
                print "G4 P%d" %self.stop_delay 
                print "G1 X" + str(x_pos) + " Y" + str(y_pos) + " F" + self.feed_rate
                
   
    ###################################
    #
    ###################################
    def output_rect_fill_GCODE(self, x_pos, y_pos, x_dim, y_dim, x_hole_dim, y_hole_dim) :
        #check values
        if x_dim != None and y_dim != None:
            print "(FILL)"
            fill_current_x_dim = float(x_dim) - self.line_width
            fill_current_y_dim = float(y_dim) - self.line_width
            if x_hole_dim == None:
                while fill_current_x_dim > 0 and fill_current_y_dim > 0:
                    self.output_rectangle_GCODE(x_pos, y_pos, fill_current_x_dim, fill_current_y_dim, None, None)
                    fill_current_x_dim -= self.line_width
                    fill_current_y_dim -= self.line_width
                    
            ############
            #NOT YET IMPLEMENTED: HOLES
            ############
            
            #if x_hole_dim != None and y_hole_dim == None:
                #circular hole
            #    while fill_current_x_dim > x_hole_dim:
                    #rectangular fill down to edge of circle
            #        self.output_rect_fill_GCODE(x_pos, y_pos, fill_current_x_dim, fill_current_y_dim, None, None)
            #        fill_current_x_dim -= self.line_width
            #        fill_current_y_dim -= self.line_width
                #circular fill up to rectangle?
                
               
    #########################################
    #
    #########################################
    def output_circle_fill_GCODE(self, x_pos, y_pos, outer_diameter, x_hole_dim, y_hole_dim) :
        #check values
        if outer_diameter != None:
            print "(FILL)"
            fill_current_diameter = float(outer_diameter) - self.line_width
            
            if x_hole_dim != None:
                fill_minimum_diameter = float(x_hole_dim)
            else:
                fill_minimum_diameter = 0
            ##########
            #NOT YET IMPLEMENTED: SQUARE HOLES
            #if y_hole_dim != None:
            #    fill_minimum_y = float(y_hole_dim)
            #else: 
            #    fill_minimum_y = 0
            ##########
            
            while fill_current_diameter > fill_minimum_diameter: #or fill_current_y_dim > fill_minimum_y:
                self.output_circle_GCODE(x_pos, y_pos, fill_current_diameter, None, None)
                #NEEDS WORK
                #if fill_current_diameter > fill_minimum_diameter:
                fill_current_diameter -= self.line_width
            
            
    def output_GCODE(self):
        
        current_general_command = None 
        current_draw_command = None
        current_draft_command = None
        
        macros = [] 
        apature_defs = [] 
       
        if(self.format_statement_command.coordinate_notation == GerberConstants.fs_absolute_coords):
            print "G90"
        elif(self.format_statement_command.coordinate_notation == GerberConstants.fs_incremental_coords):
            print "G91"
        else:
            print "NO incremental or absolute coords bail out!"
            return 
           
        for gerber_command in self.gerber_commands:
            if( gerber_command.command == None ): 
                continue 
            
            if( gerber_command.command_type == "c" ):
                gcode_line = "G1 "  
                
                if( gerber_command.command.x != None ):
                    current_x_pos = gerber_command.command.x
                    gcode_line += "X" + gerber_command.command.x + " " 
                    
                if( gerber_command.command.y != None ): 
                    current_y_pos = gerber_command.command.y
                    gcode_line += "Y" + gerber_command.command.y + " " 
                    
                if( gerber_command.command.z != None ): 
                    current_z_pos = gerber_command.command.z
                    gcode_line += "Z" + gerber_command.command.z + " " 
                    
                gcode_line += "F" + self.feed_rate
                    
                if( gerber_command.command.d != None ):
                  
                    if(current_draw_command != gerber_command.command.d or 
                       gerber_command.command.d == GerberConstants.d_flash_aperature):

                        current_draw_command = gerber_command.command.d  
                    
                        if( gerber_command.command.d == GerberConstants.d_exposure_on ):
                            print "M300 S%d (pen down)" %self.servo_down
                            print "G4 P%d" %self.start_delay
                      
                        if( gerber_command.command.d == GerberConstants.d_exposure_off ):
                            print "M300 S%d (pen up)" %self.servo_up
                            print "G4 P%d" %self.stop_delay
                            
                        if( gerber_command.command.d == GerberConstants.d_flash_aperature ):
                            print "M300 S%d (pen up)" %self.servo_up
                            print "G4 P%d" %self.stop_delay
     
                print gcode_line
                
                if( gerber_command.command.d != None ):
                    if( gerber_command.command.d == GerberConstants.d_flash_aperature ):
                        if apature_def.apature_type == "R" :
                            print "(RECTANGLE)"
                            self.output_rect_fill_GCODE(float(current_x_pos), float(current_y_pos), 
                                                        apature_def.X_dim, apature_def.Y_dim, 
                                                        apature_def.X_hole_dim, apature_def.Y_hole_dim)
                            
                        if apature_def.apature_type == "C" :
                            print "(CIRCLE)"
                            self.output_circle_fill_GCODE(float(current_x_pos), float(current_y_pos), 
                                                        apature_def.outside_diameter,
                                                        apature_def.X_hole_dim, apature_def.Y_hole_dim)
                            
                        if apature_def.apature_type == "O" :
                            print "(OVAL)"
                            self.output_oval_GCODE(float(current_x_pos), float(current_y_pos), 
                                                   apature_def.X_dim, apature_def.Y_dim, 
                                                   apature_def.X_hole_dim, apature_def.Y_hole_dim)
                            
                        
                        #if apature_def.macro = self.apature_macros["OC8"]
                        #    print "(AM POLYGON)"
                        #    self.output_polygon_GCODE(float(current_x_pos), float(current_y_pos),
                        #                              float(self.apature_macro.vertices), float(apature_def.outside_diameter),
                        #                              float(self.apature_macro.rotation))
                           
                            
                
            if( gerber_command.command_type == "g" ):
                gcode_line = "G" 
                
                if(gerber_command.command.general_type == GerberConstants.g_inches):
                    gcode_line += "20" 
                elif ( gerber_command.command.general_type == GerberConstants.g_millimeters):
                    gcode_line += "21"
                else : 
                    gcode_line += gerber_command.command.general_type
                    
                print gcode_line 
                  
                    
                current_general_command = gerber_command.command 
                
            if (gerber_command.command_type == "d") :
                print "(*********" + gerber_command.command.draft_type + ")"
                
                apature_def = self.apature_definitions[gerber_command.command.draft_type]
                print "(" + apature_def.apature_type + ")"
                   
            if( gerber_command.command_type == "m" ):
                if gerber_command.command.machine_type == GerberConstants.m_end: #end of program
                    print "M300 S%d (pen up)" %self.servo_up
                    print "G4 P500"
                    print "G1 X0 Y0 F3500.00 (end of program, go home)"
                        
                        
                
        
            
             
