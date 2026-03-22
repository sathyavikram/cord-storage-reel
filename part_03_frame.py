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

def build_frame(z_plane, is_left):
    P_hub = App.Vector(0, 0, z_plane)
    P_f = App.Vector(x_spread, y_floor, z_plane)
    P_b = App.Vector(-x_spread, y_floor, z_plane)
    P_t = App.Vector(0, y_top, z_plane)

    def make_strut(p1, p2):
        v = p2 - p1
        L = v.Length
        box = Part.makeBox(L, frame_width, hub_thickness, App.Vector(0, -frame_width/2, -hub_thickness/2))
        c1 = Part.makeCylinder(frame_width/2, hub_thickness, App.Vector(0,0,-hub_thickness/2))
        c2 = Part.makeCylinder(frame_width/2, hub_thickness, App.Vector(L,0,-hub_thickness/2))
        strut = box.fuse(c1).fuse(c2)
        angle = math.degrees(math.atan2(v.y, v.x))
        strut.Placement = App.Placement(p1, App.Rotation(App.Vector(0,0,1), angle))
        return strut

    s1 = make_strut(P_hub, P_f)
    s2 = make_strut(P_hub, P_b)
    s3 = make_strut(P_f, P_b)
    s4 = make_strut(P_hub, P_t)
    ring = Part.makeCylinder(hub_radius, hub_thickness, P_hub - App.Vector(0,0,hub_thickness/2))
    frame = s1.fuse(s2).fuse(s3).fuse(s4).fuse(ring)
    
    hole = Part.makeCylinder(hub_hole_radius, hub_thickness + 10, P_hub - App.Vector(0,0,hub_thickness/2 + 5))
    
    # Female Anchor parameters
    nest_depth = 5.0 * scale
    anchor_length = 20.0 * scale
    
    hole_radius = 9.0 * scale
    core_radius = hole_radius - (1.5 * scale)
    rib_height = 5.0 * scale
    clearance = 0.25 * scale # slightly larger clearance for easy lock
    rib_flare_radius = hole_radius + (0.6 * scale) + clearance
    rib_base_radius = core_radius + clearance

    # Base cutter built facing +Z
    base_cutter = Part.makeCylinder(core_radius + clearance, anchor_length, App.Vector(0,0,0), App.Vector(0,0,1))
    current_z = 0.0
    while current_z + rib_height <= anchor_length:
        rib = Part.makeCone(rib_flare_radius, rib_base_radius, rib_height, App.Vector(0,0,current_z), App.Vector(0,0,1))
        base_cutter = base_cutter.fuse(rib)
        current_z += rib_height
        
    tip_height = anchor_length - current_z
    if tip_height > 0.01:
        tip_cone = Part.makeCone(rib_flare_radius, core_radius - (1.0*scale) + clearance, tip_height, App.Vector(0,0,current_z), App.Vector(0,0,1))
        base_cutter = base_cutter.fuse(tip_cone)

    def make_socket(pos):
        if is_left:
            v_dir = App.Vector(0,0,1)
            inner_face_z = pos.z + hub_thickness/2
            # Nest starts at inner_face_z and goes -Z for nest_depth
            nest_z = inner_face_z - nest_depth
            nest = Part.makeCylinder(crossbar_radius + clearance, nest_depth + 1.0, App.Vector(pos.x, pos.y, nest_z), v_dir)
            
            # Female anchor hole starts at nest_z and goes -Z for anchor_length
            cutter = base_cutter.copy()
            cutter.Placement = App.Placement(App.Vector(pos.x, pos.y, nest_z), App.Rotation(App.Vector(1,0,0), 180)) # Points -Z
            
        else:
            v_dir = App.Vector(0,0,1)
            inner_face_z = pos.z - hub_thickness/2
            # Nest starts at inner_face_z and goes +Z for nest_depth. 
            nest = Part.makeCylinder(crossbar_radius + clearance, nest_depth + 1.0, App.Vector(pos.x, pos.y, inner_face_z - 0.5), v_dir)
            
            # Female anchor hole starts at inner_face_z + nest_depth
            anchor_z = inner_face_z + nest_depth
            cutter = base_cutter.copy()
            cutter.Placement = App.Placement(App.Vector(pos.x, pos.y, anchor_z), App.Rotation(0,0,0,1)) # Points +Z
            
        return nest.fuse(cutter)

    sock1 = make_socket(P_f)
    sock2 = make_socket(P_b)
    sock3 = make_socket(P_t)
    
    return frame.cut(hole).cut(sock1).cut(sock2).cut(sock3).removeSplitter()

def build_right_frame():
    return build_frame(z_R, False)

def build_left_frame():
    return build_frame(z_L, True)

if __name__ == '__main__':
    import FreeCAD as App
    import Part
    import os

    doc_name = "Doc_" + os.path.basename(__file__).replace(".py", "")
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

    p_03_Frame_Right = build_right_frame()
    Part.show(p_03_Frame_Right, 'RightFrame')
    print(f'Exporting 03_Frame_Right...')
    p_03_Frame_Right.exportStl(os.path.join(export_dir, '03_Frame_Right.stl'))
    p_03_Frame_Right.exportStep(os.path.join(export_dir, '03_Frame_Right.step'))
    p_03_Frame_Left = build_left_frame()
    Part.show(p_03_Frame_Left, 'LeftFrame')
    print(f'Exporting 03_Frame_Left...')
    p_03_Frame_Left.exportStl(os.path.join(export_dir, '03_Frame_Left.stl'))
    p_03_Frame_Left.exportStep(os.path.join(export_dir, '03_Frame_Left.step'))
