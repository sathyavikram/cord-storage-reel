import sys, os
try:
    _script_dir = os.path.dirname(os.path.abspath(__file__))
except NameError:
    _script_dir = "/Users/intelligentmachine/Documents/workspace/3d-models/cord-storage-reel-v3"
if _script_dir not in sys.path:
    sys.path.insert(0, _script_dir)
import FreeCAD as App
import Part
from params import *

def build_handle():
    h_z = half_axle + flange_thickness 
    h_peg = Part.makeCylinder(handle_peg_radius, flange_thickness, App.Vector(hole_dist, 0, h_z - flange_thickness))
    h_shield = Part.makeCylinder(22*scale, 8*scale, App.Vector(hole_dist, 0, h_z)) 
    h_grip = Part.makeCylinder(14*scale, 65*scale, App.Vector(hole_dist, 0, h_z + 8*scale))
    return h_peg.fuse(h_shield).fuse(h_grip).removeSplitter()

if __name__ == '__main__':
    import FreeCAD as App
    import Part
    import os

    doc_name = "Doc_" + os.path.basename(__file__).replace(".py", "")
    doc = App.newDocument(doc_name)

    export_dir = os.path.join(_script_dir, 'exports')
    os.makedirs(export_dir, exist_ok=True)

    p_02_Handle = build_handle()
    Part.show(p_02_Handle, 'Handle')
    print(f'Exporting 02_Handle...')
    p_02_Handle.exportStl(os.path.join(export_dir, '02_Handle.stl'))
    p_02_Handle.exportStep(os.path.join(export_dir, '02_Handle.step'))
