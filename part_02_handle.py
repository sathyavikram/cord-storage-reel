import sys, os, math
try:
    _script_dir = os.path.dirname(os.path.abspath(__file__))
except NameError:
    _script_dir = os.getcwd()
_helpers_dir = os.path.join(os.path.dirname(_script_dir), 'helpers')
if _script_dir not in sys.path:
    sys.path.insert(0, _script_dir)
if _helpers_dir not in sys.path:
    sys.path.insert(0, _helpers_dir)
import FreeCAD as App
import Part
import sys
if "params" in sys.modules: del sys.modules["params"]
from params import *

def build_handle():
    x_mount = frame_handle_mount_x
    y_mount = frame_handle_mount_y
    z_crank = right_frame_outer_z + handle_standoff
    crank_thickness = 10 * scale
    handle_anchor_len = 20 * scale
    
    socket_radius = handle_peg_radius + clearance
    sock_outer_rad = pin_radius
    
    standoff = Part.makeCylinder(sock_outer_rad, handle_standoff, App.Vector(x_mount, y_mount, right_frame_outer_z))
    socket_body = Part.makeCylinder(sock_outer_rad, crank_thickness + handle_anchor_len + 5*scale, App.Vector(x_mount, y_mount, z_crank))
    
    arm_width = 36 * scale
    arm_box = Part.makeBox(arm_width, hole_dist, crank_thickness, App.Vector(x_mount - arm_width/2, y_mount, z_crank))
    arm_rounded = Part.makeCylinder(arm_width/2, crank_thickness, App.Vector(x_mount, y_mount + hole_dist, z_crank))
    
    crank_solid = standoff.fuse(socket_body).fuse(arm_box).fuse(arm_rounded)
    
    h_clearance = 0.4 * scale
    def make_hex_prism(radius, length, placement):
        import math
        pts = []
        for i in range(7):
            angle = i * (math.pi / 3)
            pts.append(App.Vector(radius * math.cos(angle), radius * math.sin(angle), 0))
        face = Part.Face(Part.Wire(Part.makePolygon(pts)))
        prism = face.extrude(App.Vector(0, 0, length))
        prism.Placement = placement
        return prism
        
    hex_hole_len = handle_standoff + crank_thickness
    hex_cutout = make_hex_prism(handle_peg_radius + h_clearance, hex_hole_len + 1, App.Placement(App.Vector(x_mount, y_mount, right_frame_outer_z - 0.5), App.Rotation(0,0,0,1)))
    
    handle_top_z = z_crank + crank_thickness + handle_anchor_len + 5*scale
    
    # Simple smooth hole for the Universal Cap thread to pass through
    pass_through_radius = 12.0 * scale + h_clearance + 0.5 * scale  # A bit extra clearance so it freely spins
    pass_through_hole = Part.makeCylinder(pass_through_radius, 100 * scale, App.Vector(x_mount, y_mount, right_frame_outer_z - 5*scale))
    
    pin_cutout = hex_cutout.fuse(pass_through_hole)
    crank_arm = crank_solid.cut(pin_cutout)
    
    h_shield = Part.makeCylinder(28*scale, 8*scale, App.Vector(x_mount, y_mount + hole_dist, z_crank + crank_thickness))
    h_grip = Part.makeCylinder(18*scale, 65*scale, App.Vector(x_mount, y_mount + hole_dist, z_crank + crank_thickness + 8*scale))
    
    handle = crank_arm.fuse(h_shield).fuse(h_grip).removeSplitter()
    
    handle.rotate(App.Vector(x_mount, y_mount, 0), App.Vector(0,0,1), 0)
    
    export_dir = EXPORT_DIR
    os.makedirs(export_dir, exist_ok=True)
    stl_file = os.path.join(export_dir, 'part_02_handle.stl')
    step_file = os.path.join(export_dir, 'part_02_handle.step')
    for f_path in [stl_file, step_file]:
        if os.path.exists(f_path):
            os.remove(f_path)
    print(f'Exporting part_02_handle...')
    handle.exportStl(stl_file)
    handle.exportStep(step_file)
    
    return handle

if __name__ == '__main__':
    doc_name = 'Doc_' + os.path.basename(__file__).replace('.py', '')
    try:
        doc = App.getDocument(doc_name)
    except Exception:
        doc = None
    if doc is not None:
        for obj in doc.Objects:
            doc.removeObject(obj.Name)
    else:
        doc = App.newDocument(doc_name)

    p_02_Handle = build_handle()
    Part.show(p_02_Handle, 'Handle')
