import sys, os, math
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

def build_handle():
    # Fixed handle mount point on the right frame (not spool-mounted).
    x_mount = frame_handle_mount_x
    y_mount = frame_handle_mount_y
    z_crank = right_frame_outer_z + handle_standoff
    crank_thickness = 10 * scale
    
    socket_radius = handle_peg_radius + clearance
    sock_outer_rad = handle_peg_radius + 10 * scale
    
    standoff = Part.makeCylinder(sock_outer_rad, handle_standoff, App.Vector(x_mount, y_mount, right_frame_outer_z))
    socket_body = Part.makeCylinder(sock_outer_rad, crank_thickness, App.Vector(x_mount, y_mount, z_crank))
    
    arm_box = Part.makeBox(20*scale, hole_dist, crank_thickness, App.Vector(x_mount - 10*scale, y_mount, z_crank))
    arm_rounded = Part.makeCylinder(10*scale, crank_thickness, App.Vector(x_mount, y_mount + hole_dist, z_crank))
    crank_solid = standoff.fuse(socket_body).fuse(arm_box).fuse(arm_rounded)
    
    pin_cutout = Part.makeCylinder(socket_radius, crank_thickness + handle_standoff, App.Vector(x_mount, y_mount, right_frame_outer_z))
    crank_arm = crank_solid.cut(pin_cutout)
    
    h_shield = Part.makeCylinder(22*scale, 8*scale, App.Vector(x_mount, y_mount + hole_dist, z_crank + crank_thickness))
    h_grip = Part.makeCylinder(14*scale, 65*scale, App.Vector(x_mount, y_mount + hole_dist, z_crank + crank_thickness + 8*scale))
    
    handle = crank_arm.fuse(h_shield).fuse(h_grip).removeSplitter()
    
    
    handle.rotate(App.Vector(x_mount, y_mount, 0), App.Vector(0,0,1), -25)
    return handle

if __name__ == '__main__':
    import FreeCAD as App
    import Part
    import os

    doc_name = 'Doc_' + os.path.basename(__file__).replace('.py', '')
    doc = App.newDocument(doc_name)

    export_dir = EXPORT_DIR
    os.makedirs(export_dir, exist_ok=True)

    p_02_Handle = build_handle()
    Part.show(p_02_Handle, 'Handle')
    print(f'Exporting 02_Handle...')
    p_02_Handle.exportStl(os.path.join(export_dir, '02_Handle.stl'))
    p_02_Handle.exportStep(os.path.join(export_dir, '02_Handle.step'))
