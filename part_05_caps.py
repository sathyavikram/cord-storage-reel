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
    cap_rad = hub_radius

    # Left Cap Only (Snaps onto left anchor)
    anchor_length = 20.0 * scale
    
    c_hole_radius = 18.0 * scale
    c_core_radius = c_hole_radius - (1.5 * scale)
    c_rib_height = 5.0 * scale
    c_clearance = 0.4 * scale
    z_clearance = 0.2 * scale
    c_rib_flare_radius = c_hole_radius + (0.6 * scale) + c_clearance
    c_rib_base_radius = c_core_radius + c_clearance

    # We want a 5mm visual gap between the outside of the frame and the cap
    left_axle_pin_length = z_gap + hub_thickness + (5.0 * scale)
    anchor_tip_z = -half_axle - flange_thickness - left_axle_pin_length
    
    # Push the cap's bottom out further so the geometry actually leaves a 5mm gap
    z_cap_bottom_L = anchor_tip_z - anchor_length - 5*scale
    
    # Cap body needs to be tall enough to house the 20mm socket + outer wall
    cap_h = anchor_length + 5*scale
    cap_L = Part.makeCylinder(cap_rad, cap_h, App.Vector(0,0, z_cap_bottom_L))
    
    c_L_sock = Part.makeCylinder(c_core_radius + c_clearance, anchor_length + 1,
 App.Vector(0,0, anchor_tip_z - anchor_length - 0.5), App.Vector(0,0,1))
    
    curr_z = 0.0
    while curr_z + c_rib_height <= anchor_length:
        rib = Part.makeCone(c_rib_base_radius, c_rib_flare_radius, c_rib_height + z_clearance, App.Vector(0,0, anchor_tip_z - anchor_length + curr_z - z_clearance), App.Vector(0,0,1))
        c_L_sock = c_L_sock.fuse(rib)
        curr_z += c_rib_height
        
    tip_height = anchor_length - curr_z
    if tip_height > 0.01:
        tip_cone = Part.makeCone(c_rib_base_radius, c_rib_flare_radius, tip_height + z_clearance, App.Vector(0,0, anchor_tip_z - anchor_length + curr_z - z_clearance), App.Vector(0,0,1))
        c_L_sock = c_L_sock.fuse(tip_cone)

    cap_L = cap_L.cut(c_L_sock)

    return None, cap_L

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

    parts = build_caps()
    if parts[0] is not None:
        Part.show(parts[0], 'CapRight')
        print(f'Exporting 05_Cap_R...')
        parts[0].exportStl(os.path.join(export_dir, '05_Cap_R.stl'))
        parts[0].exportStep(os.path.join(export_dir, '05_Cap_R.step'))
        
    if parts[1] is not None:
        Part.show(parts[1], 'CapLeft')
        print(f'Exporting 05_Cap_L...')
        parts[1].exportStl(os.path.join(export_dir, '05_Cap_L.stl'))
        parts[1].exportStep(os.path.join(export_dir, '05_Cap_L.step'))
