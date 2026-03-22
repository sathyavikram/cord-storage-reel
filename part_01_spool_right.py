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
    
    def make_hex_prism(radius, length, placement):
        pts = []
        for i in range(7):
            angle = i * (math.pi / 3)
            pts.append(App.Vector(radius * math.cos(angle), radius * math.sin(angle), 0))
        face = Part.Face(Part.Wire(Part.makePolygon(pts)))
        prism = face.extrude(App.Vector(0, 0, length))
        prism.Placement = placement
        return prism

    r_axle_peg = make_hex_prism(peg_radius, 25 * scale, App.Placement(App.Vector(0,0,-25*scale), App.Rotation(0,0,0,1)))
    
    # --- Vertical Anchor (integrated) ---
    anchor_length = 25.0 * scale
    hole_radius = 9.0 * scale
    core_radius = hole_radius - (1.5 * scale)
    rib_height = 5.0 * scale
    
    rib_flare_radius = hole_radius + (0.6 * scale)
    rib_base_radius = core_radius

    # The anchor starts at Z=-50 and builds UP to Z=-25.
    # The tip is at -50. It must narrow at the tip and flare as Z increases towards the spool base.
    snap_peg = Part.makeCylinder(core_radius, anchor_length, App.Vector(0,0,-50*scale), App.Vector(0,0,1))
    
    current_z = -50.0 * scale
    while current_z + rib_height <= -25.0 * scale + 0.01:
        # radius1 (at current_z) = small, radius2 (at top) = large
        rib = Part.makeCone(rib_base_radius, rib_flare_radius, rib_height, App.Vector(0,0,current_z), App.Vector(0,0,1))
        snap_peg = snap_peg.fuse(rib)
        current_z += rib_height
        
    tip_height = (-25.0 * scale) - current_z
    if tip_height > 0.01:
        tip_cone = Part.makeCone(rib_base_radius, rib_flare_radius, tip_height, App.Vector(0,0,current_z), App.Vector(0,0,1))
        snap_peg = snap_peg.fuse(tip_cone)

    cut_w = 2.0 * scale
    cut_h = anchor_length + 2.0 * scale
    box_s = 40.0 * scale
    c1 = Part.makeBox(box_s, cut_w, cut_h, App.Vector(-box_s/2, -cut_w/2, -51.0 * scale))
    c2 = Part.makeBox(cut_w, box_s, cut_h, App.Vector(-cut_w/2, -box_s/2, -51.0 * scale))
    snap_peg = snap_peg.cut(c1).cut(c2)

    r_axle_peg = r_axle_peg.fuse(snap_peg)

    pin_base = App.Vector(0,0, half_axle + flange_thickness)
    r_pin = Part.makeCylinder(hub_hole_radius - clearance, right_axle_pin_length, pin_base)
    
    # --- Hex Handle Peg & Anchor Tip ---
    handle_hex_len = handle_standoff + 10 * scale
    r_handle_hex = make_hex_prism(handle_peg_radius, handle_hex_len, App.Placement(pin_base + App.Vector(0,0, right_axle_pin_length), App.Rotation(0,0,0,1)))
    
    handle_anchor_len = 20 * scale
    h_hole_radius = handle_peg_radius - 1.0 * scale
    h_core_radius = h_hole_radius - (1.5 * scale)
    h_rib_height = 4.0 * scale
    h_rib_flare_radius = h_hole_radius + (0.5 * scale)
    h_rib_base_radius = h_core_radius
    
    anchor_base_z = (pin_base + App.Vector(0,0, right_axle_pin_length)).z + handle_hex_len
    h_snap_peg = Part.makeCylinder(h_core_radius, handle_anchor_len, App.Vector(0,0,anchor_base_z), App.Vector(0,0,1))
    
    curr_z = 0.0
    while curr_z + h_rib_height <= handle_anchor_len:
        rib = Part.makeCone(h_rib_base_radius, h_rib_flare_radius, h_rib_height, App.Vector(0,0,anchor_base_z + curr_z), App.Vector(0,0,1))
        h_snap_peg = h_snap_peg.fuse(rib)
        curr_z += h_rib_height
        
    tip_height = handle_anchor_len - curr_z
    if tip_height > 0.01:
        tip_cone = Part.makeCone(h_rib_base_radius, h_rib_flare_radius, tip_height, App.Vector(0,0,anchor_base_z + curr_z), App.Vector(0,0,1))
        h_snap_peg = h_snap_peg.fuse(tip_cone)

    cut_w = 2.0 * scale
    cut_h = handle_anchor_len + 2.0 * scale
    box_s = 40.0 * scale
    c1 = Part.makeBox(box_s, cut_w, cut_h, App.Vector(-box_s/2, -cut_w/2, anchor_base_z - 1.0))
    c2 = Part.makeBox(cut_w, box_s, cut_h, App.Vector(-cut_w/2, -box_s/2, anchor_base_z - 1.0))
    h_snap_peg = h_snap_peg.cut(c1).cut(c2)

    r_handle_peg = r_handle_hex.fuse(h_snap_peg)

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

    p_01_Spool_Right = build_right_spool()
    Part.show(p_01_Spool_Right, 'RightSpool')
    print(f'Exporting 01_Spool_Right...')
    p_01_Spool_Right.exportStl(os.path.join(export_dir, '01_Spool_Right.stl'))
    p_01_Spool_Right.exportStep(os.path.join(export_dir, '01_Spool_Right.step'))
