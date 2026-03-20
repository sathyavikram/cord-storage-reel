import sys, os
try:
    _script_dir = os.path.dirname(os.path.abspath(__file__))
except NameError:
    _script_dir = os.getcwd()
if _script_dir not in sys.path:
    sys.path.insert(0, _script_dir)
import FreeCAD as App
import Part
import math
import sys
if "params" in sys.modules: del sys.modules["params"]
from params import *

def build_left_spool():
    l_flange = Part.makeCylinder(flange_radius, flange_thickness, App.Vector(0,0, -half_axle - flange_thickness))
    l_axle = Part.makeCylinder(axle_radius, half_axle, App.Vector(0,0,-half_axle))
    
    l_axle_hole = Part.makeCylinder(peg_radius + clearance, 30*scale, App.Vector(0,0,-26*scale)) 
    l_pin = Part.makeCylinder(pin_radius, left_pin_length, App.Vector(0,0, -half_axle - flange_thickness - left_pin_length))

    for i in range(6):
        angle = math.radians(i * 60)
        hx = hole_dist * math.cos(angle)
        hy = hole_dist * math.sin(angle)
        cutter = Part.makeCylinder(hole_radius, flange_thickness + 10, App.Vector(hx, hy, -half_axle - flange_thickness - 5))
        l_flange = l_flange.cut(cutter)
        
    left_spool = l_flange.fuse(l_axle).fuse(l_pin).cut(l_axle_hole)
    return left_spool.removeSplitter()

if __name__ == '__main__':
    import FreeCAD as App
    import Part
    import os

    doc_name = "Doc_" + os.path.basename(__file__).replace(".py", "")
    doc = App.newDocument(doc_name)

    export_dir = EXPORT_DIR
    os.makedirs(export_dir, exist_ok=True)

    p_01_Spool_Left = build_left_spool()
    Part.show(p_01_Spool_Left, 'LeftSpool')
    print(f'Exporting 01_Spool_Left...')
    p_01_Spool_Left.exportStl(os.path.join(export_dir, '01_Spool_Left.stl'))
    p_01_Spool_Left.exportStep(os.path.join(export_dir, '01_Spool_Left.step'))
