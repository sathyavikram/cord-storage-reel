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

def build_right_spool():
    r_flange = Part.makeCylinder(flange_radius, flange_thickness, App.Vector(0,0, half_axle))
    r_axle = Part.makeCylinder(axle_radius, half_axle, App.Vector(0,0,0))
    
    r_axle_peg = Part.makeCylinder(peg_radius, 25*scale, App.Vector(0,0,-25*scale))
    pin_base = App.Vector(0,0, half_axle + flange_thickness)
    r_pin = Part.makeCylinder(pin_radius, right_axle_pin_length, pin_base)
    r_handle_peg = Part.makeCylinder(
        handle_peg_radius,
        handle_peg_length,
        pin_base + App.Vector(0,0, right_axle_pin_length),
    )

    for i in range(6):
        angle = math.radians(i * 60)
        hx = hole_dist * math.cos(angle)
        hy = hole_dist * math.sin(angle)
        cutter = Part.makeCylinder(hole_radius, flange_thickness + 10, App.Vector(hx, hy, half_axle - 5))
        r_flange = r_flange.cut(cutter)

    right_spool = r_flange.fuse(r_axle).fuse(r_axle_peg).fuse(r_pin).fuse(r_handle_peg)
    return right_spool.removeSplitter()

if __name__ == '__main__':
    import FreeCAD as App
    import Part
    import os

    doc_name = "Doc_" + os.path.basename(__file__).replace(".py", "")
    doc = App.newDocument(doc_name)

    export_dir = EXPORT_DIR
    os.makedirs(export_dir, exist_ok=True)

    p_01_Spool_Right = build_right_spool()
    Part.show(p_01_Spool_Right, 'RightSpool')
    print(f'Exporting 01_Spool_Right...')
    p_01_Spool_Right.exportStl(os.path.join(export_dir, '01_Spool_Right.stl'))
    p_01_Spool_Right.exportStep(os.path.join(export_dir, '01_Spool_Right.step'))
