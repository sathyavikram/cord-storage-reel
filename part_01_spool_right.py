import sys, os
try:
    _script_dir = os.path.dirname(os.path.abspath(__file__))
except NameError:
    _script_dir = "/Users/intelligentmachine/Documents/workspace/3d-models/cord-storage-reel-v3"
if _script_dir not in sys.path:
    sys.path.insert(0, _script_dir)
import FreeCAD as App
import Part
import math
from params import *

def build_right_spool():
    r_flange = Part.makeCylinder(flange_radius, flange_thickness, App.Vector(0,0, half_axle))
    r_axle = Part.makeCylinder(axle_radius, half_axle, App.Vector(0,0,0))
    
    r_axle_peg = Part.makeCylinder(peg_radius, 25*scale, App.Vector(0,0,-25*scale))
    r_pin = Part.makeCylinder(pin_radius, pin_length, App.Vector(0,0, half_axle + flange_thickness))

    for i in range(6):
        angle = math.radians(i * 60)
        hx = hole_dist * math.cos(angle)
        hy = hole_dist * math.sin(angle)
        cutter = Part.makeCylinder(hole_radius, flange_thickness + 10, App.Vector(hx, hy, half_axle - 5))
        r_flange = r_flange.cut(cutter)

    handle_hole = Part.makeCylinder(handle_peg_radius + clearance, flange_thickness + 10, App.Vector(hole_dist, 0, half_axle - 5))
    r_flange = r_flange.cut(handle_hole)

    right_spool = r_flange.fuse(r_axle).fuse(r_axle_peg).fuse(r_pin)
    return right_spool.removeSplitter()

if __name__ == '__main__':
    import FreeCAD as App
    import Part
    import os

    doc = App.ActiveDocument
    if not doc:
        doc = App.newDocument('ExportDoc')

    export_dir = os.path.join(_script_dir, 'exports')
    os.makedirs(export_dir, exist_ok=True)

    p_01_Spool_Right = build_right_spool()
    Part.show(p_01_Spool_Right, 'RightSpool')
    print(f'Exporting 01_Spool_Right...')
    p_01_Spool_Right.exportStl(os.path.join(export_dir, '01_Spool_Right.stl'))
    p_01_Spool_Right.exportStep(os.path.join(export_dir, '01_Spool_Right.step'))
