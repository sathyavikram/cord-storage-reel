import sys, os
try:
    _script_dir = os.path.dirname(os.path.abspath(__file__))
except NameError:
    _script_dir = os.getcwd()
if _script_dir not in sys.path:
    sys.path.insert(0, _script_dir)
import FreeCAD as App
import Part
import sys
if "params" in sys.modules: del sys.modules["params"]
from params import *

def build_caps():
    cap_thickness = 10 * scale
    cap_rad = pin_radius + 12 * scale

    z_cap_bottom_R = half_axle + flange_thickness + right_pin_length - (cap_thickness - 3*scale)
    cap_R = Part.makeCylinder(cap_rad, cap_thickness, App.Vector(0,0, z_cap_bottom_R))
    c_R_sock = Part.makeCylinder(handle_peg_radius + clearance, cap_thickness - 3*scale, App.Vector(0,0, z_cap_bottom_R))
    cap_R = cap_R.cut(c_R_sock)

    z_cap_bottom_L = -half_axle - flange_thickness - left_pin_length + (cap_thickness - 3*scale)
    cap_L = Part.makeCylinder(cap_rad, cap_thickness, App.Vector(0,0, z_cap_bottom_L - cap_thickness))
    c_L_sock = Part.makeCylinder(pin_radius + clearance, cap_thickness - 3*scale, App.Vector(0,0, z_cap_bottom_L - (cap_thickness - 3*scale)))
    cap_L = cap_L.cut(c_L_sock)

    return cap_R, cap_L

if __name__ == '__main__':
    import FreeCAD as App
    import Part
    import os

    doc_name = "Doc_" + os.path.basename(__file__).replace(".py", "")
    doc = App.newDocument(doc_name)

    export_dir = EXPORT_DIR
    os.makedirs(export_dir, exist_ok=True)

    parts = build_caps()
    Part.show(parts[0], 'CapRight')
    print(f'Exporting 05_Cap_R...')
    parts[0].exportStl(os.path.join(export_dir, '05_Cap_R.stl'))
    parts[0].exportStep(os.path.join(export_dir, '05_Cap_R.step'))
    Part.show(parts[1], 'CapLeft')
    print(f'Exporting 05_Cap_L...')
    parts[1].exportStl(os.path.join(export_dir, '05_Cap_L.stl'))
    parts[1].exportStep(os.path.join(export_dir, '05_Cap_L.step'))
