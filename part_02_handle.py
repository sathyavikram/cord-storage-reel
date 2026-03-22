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
    x_mount = frame_handle_mount_x
    y_mount = frame_handle_mount_y
    z_crank = right_frame_outer_z + handle_standoff
    crank_thickness = 10 * scale
    handle_anchor_len = 20 * scale
    
    socket_radius = handle_peg_radius + clearance
    sock_outer_rad = handle_peg_radius + 10 * scale
    
    # Make the central hub taller to house the internal snap lock socket
    standoff = Part.makeCylinder(sock_outer_rad, handle_standoff, App.Vector(x_mount, y_mount, right_frame_outer_z))
    socket_body = Part.makeCylinder(sock_outer_rad, crank_thickness + handle_anchor_len + 5*scale, App.Vector(x_mount, y_mount, z_crank))
    
    arm_box = Part.makeBox(24*scale, hole_dist, crank_thickness, App.Vector(x_mount - 12*scale, y_mount, z_crank))
    arm_rounded = Part.makeCylinder(12*scale, crank_thickness, App.Vector(x_mount, y_mount + hole_dist, z_crank))
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
    
    # Internal Ribbed Socket
    h_hole_radius = handle_peg_radius - 1.0 * scale
    h_core_radius = h_hole_radius - (1.5 * scale)
    h_rib_height = 4.0 * scale
    h_rib_flare_radius = h_hole_radius + (0.5 * scale) + h_clearance
    h_rib_base_radius = h_core_radius + h_clearance
    
    anchor_base_z = right_frame_outer_z + hex_hole_len
    snap_socket = Part.makeCylinder(h_core_radius + h_clearance, handle_anchor_len + 1, App.Vector(x_mount, y_mount, anchor_base_z - 0.5), App.Vector(0,0,1))
    
    curr_z = 0.0
    while curr_z + h_rib_height <= handle_anchor_len:
        rib = Part.makeCone(h_rib_base_radius, h_rib_flare_radius, h_rib_height, App.Vector(x_mount, y_mount, anchor_base_z + curr_z), App.Vector(0,0,1))
        snap_socket = snap_socket.fuse(rib)
        curr_z += h_rib_height
        
    tip_height = handle_anchor_len - curr_z
    if tip_height > 0.01:
        tip_cone = Part.makeCone(h_rib_base_radius, h_rib_flare_radius, tip_height, App.Vector(x_mount, y_mount, anchor_base_z + curr_z), App.Vector(0,0,1))
        snap_socket = snap_socket.fuse(tip_cone)
        
    pin_cutout = hex_cutout.fuse(snap_socket)
    crank_arm = crank_solid.cut(pin_cutout)
    
    h_shield = Part.makeCylinder(28*scale, 8*scale, App.Vector(x_mount, y_mount + hole_dist, z_crank + crank_thickness))
    h_grip = Part.makeCylinder(18*scale, 65*scale, App.Vector(x_mount, y_mount + hole_dist, z_crank + crank_thickness + 8*scale))
    handle = crank_arm.fuse(h_shield).fuse(h_grip).removeSplitter()
    
    handle.rotate(App.Vector(x_mount, y_mount, 0), App.Vector(0,0,1), 0)
    return handle

if __name__ == '__main__':
    import FreeCAD as App
    import Part
    import os

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

    export_dir = EXPORT_DIR
    os.makedirs(export_dir, exist_ok=True)

    p_02_Handle = build_handle()
    Part.show(p_02_Handle, 'Handle')
    print(f'Exporting 02_Handle...')
    p_02_Handle.exportStl(os.path.join(export_dir, '02_Handle.stl'))
    p_02_Handle.exportStep(os.path.join(export_dir, '02_Handle.step'))
