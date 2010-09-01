import sys
import entities
import context
from math import radians

class RegisterMap:
    def __init__(self):
        self.map = {}
    def add(self,code,value):
        if code in self.map:
            entry = self.map[code]
            if isinstance(entry, list):
                entry.append(value)
            else:
                self.map[code] = [entry, value]
        else:
            self.map[code] = value
    def __getitem__(self,key):
        return self.map[key]
    def get_float(self,code,default = 0.0):
        if code in self.map:
            return float(self.map[code])
        return default
    def get_angle(self,code,default = 0.0):
        "Returns angle in radians"
        if code in self.map:
            return radians(float(self.map[code]))
        return default
class DXFLine(entities.Line):
    def load(self,emap):
        self.thickness = emap.get_float(39)
        self.start = (emap.get_float(10),emap.get_float(20))
        self.end = (emap.get_float(11),emap.get_float(21))

class DXFCircle(entities.Circle):
    def load(self,emap):
        self.center = (emap.get_float(10),emap.get_float(20))
        self.radius = emap.get_float(40)
    def __str__(self):
        return "Circle at (%f,%f), radius %f" % \
            (self.center[0], self.center[1], self.radius)

class DXFArc(entities.Arc):
    def load(self,emap):
        self.center = (emap.get_float(10),emap.get_float(20))
        self.radius = emap.get_float(40)
        self.start_angle = emap.get_angle(50)
        self.end_angle = emap.get_angle(51)

class DXFEllipse(entities.Ellipse):
    def load(self,emap):
        self.center = (emap.get_float(10),emap.get_float(20))
        # major axis relative to center
        self.major = (emap.get_float(11),emap.get_float(21))
        self.minor_to_major = emap.get_float(40)
        self.start_param = emap.get_angle(50)
        self.end_param = emap.get_angle(51)

class DXFPolyLine(entities.PolyLine):
    def load(self,emap):
        self.segments = []
        self.thickness = emap.get_float(39)
        x_coords = emap.get_float(10)
        y_coords = emap.get_float(20)
        assert len(x_coords) == len(y_coords)
        self.segments = \
            [(x_coords[i],y_coords[i]) for i in range(len(x_coords))]
    
#todo: add peek functionality to handle end-of-point kinda stuff?
# This code is based on autodesk's DXF specification.
class GenericSection:
    entity_map = {
        "LINE" : DXFLine,
        "CIRCLE" : DXFCircle,
        "LWPOLYLINE" : DXFPolyLine,
        "ARC" : DXFArc,
        "ELLIPSE" : DXFEllipse
        }
    def __init__(self,parser):
        self.parser = parser
    def make_entity(self,map):
        type_name = map[0]
        if type_name in GenericSection.entity_map:
            constructor = GenericSection.entity_map[type_name]
            entity = constructor()
            entity.load(map)
            self.parser.entities.append(entity)
            

class EntitiesSection(GenericSection):
    def __init__(self,parser):
        self.parser = parser
    def make_entity(self,map):
        GenericSection.make_entity(self,map)

class BlocksSection(GenericSection):
    pass

class DxfParser:
    section_map = {
        "ENTITIES" : EntitiesSection,
        "BLOCKS" : BlocksSection
        }

    def handle_new_section(self,data):
        if data == "SECTION":
            # We need to get the section type
            (_, name) = self.get_next_code(2)
            if name in DxfParser.section_map:
                self.section = DxfParser.section_map[name](self)
            else:
                self.section = None
        elif data == "ENDSEC":
            self.section = None

    def __init__(self, stream):
        self.stream = stream
        self.entities = []
        self.blocks = []
        self.register_map = RegisterMap()
        self.section = None

    def get_next_code(self, expected_code = None):
        codeStr = self.stream.readline()
        if not codeStr:
            return
        code = int(codeStr.strip())
        value = self.stream.readline().strip()
        if expected_code:
            assert expected_code == code
        return (code,value)

    def finish_entity(self):
        if self.section:
            self.section.make_entity(self.register_map)

    def parse_next_code(self):
        code_tuple = self.get_next_code()
        if not code_tuple:
            return False
        (code,value) = code_tuple
        if code == 0:
            self.finish_entity()
            self.register_map = RegisterMap()
            self.handle_new_section(value)
        self.register_map.add(code,value)
        return True

    def parse(self):
        while self.parse_next_code():
            pass

