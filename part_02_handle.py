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
    frame_end_z = half_axle + flange_thickness + z_gap + hub_thickness
    z_crank = frame_end_z + 2*scale
    crank_thickness = 12 * scale
    
    sock_outer_rad = pin_radius + 12 * scale
    socket_body = Part.makeCylinder(sock_outer_rad, crank_thickness, App.Vector(0, 0, z_crank))
    pin_cutout = Part.makeCylinder(pin_radius + clearance, crank_thickness, App.Vector(0, 0, z_crank))
    crank_hub = socket_body.cut(pin_cutout)
    
    arm_box = Part.makeBox(20*scale, hole_dist, crank_thickness, App.Vector(-10*scale, 0, z_crank))
    arm_rounded = Part.makeCylinder(10*scale, crank_thickness, App.Vector(0, hole_dist, z_crank))
    crank_arm = crank_hub.fuse(arm_box).fuse(arm_rounded)
    
    h_shield = Part.makeCylinder(22*scale, 8*scale, App.Vector(0, hole_dist, z_crank + crank_thickness))
    h_grip = Part.makeCylinder(14*scale, 65*scale, App.Vector(0, hole_dist, z_crank + crank_thickness + 8*scale))
    
    return crank_arm.fuse(h_shield).fuse(h_grip).removeSplitter()

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
