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

def build_left_spool():
    l_flange = Part.makeCylinder(flange_radius, flange_thickness, App.Vector(0,0, -half_axle - flange_thickness))
    l_axle = Part.makeCylinder(axle_radius, half_axle, App.Vector(0,0,-half_axle))
    
    def make_hex_prism(radius, length, placement):
        pts = []
        for i in range(7):
            angle = i * (math.pi / 3)
            pts.append(App.Vector(radius * math.cos(angle), radius * math.sin(angle), 0))
        face = Part.Face(Part.Wire(Part.makePolygon(pts)))
        prism = face.extrude(App.Vector(0, 0, length))
        prism.Placement = placement
        return prism

    # The main hex receiver hole
    clearance = 0.2 * scale
    l_axle_hole = make_hex_prism(peg_radius + clearance, 26*scale, App.Placement(App.Vector(0,0,-26*scale), App.Rotation(0,0,0,1)))
    
    # --- Vertical Anchor Socket (integrated) ---
    anchor_length = 26.0 * scale
    hole_radius = 9.0 * scale
    core_radius = hole_radius - (1.5 * scale)
    rib_height = 5.0 * scale
    
    rib_flare_radius = hole_radius + (0.6 * scale) + clearance
    rib_base_radius = core_radius + clearance

    # Cutter for the female snap ribs. Extends from -52 up to -26.
    snap_socket = Part.makeCylinder(core_radius + clearance, anchor_length, App.Vector(0,0,-52*scale), App.Vector(0,0,1))
    
    current_z = -52.0 * scale
    while current_z + rib_height <= -26.0 * scale + 0.01:
        rib = Part.makeCone(rib_base_radius, rib_flare_radius, rib_height, App.Vector(0,0,current_z), App.Vector(0,0,1))
        snap_socket = snap_socket.fuse(rib)
        current_z += rib_height
        
    tip_height = (-26.0 * scale) - current_z
    if tip_height > 0.01:
        tip_cone = Part.makeCone(rib_base_radius, rib_flare_radius, tip_height, App.Vector(0,0,current_z), App.Vector(0,0,1))
        snap_socket = snap_socket.fuse(tip_cone)

    l_axle_hole = l_axle_hole.fuse(snap_socket)

    left_axle_pin_length = z_gap + hub_thickness
    l_pin_bearing = Part.makeCylinder(pin_radius, left_axle_pin_length, App.Vector(0,0, -half_axle - flange_thickness - left_axle_pin_length))
    
    # Left Anchor Tip
    anchor_length = 20.0 * scale
    c_hole_radius = 9.0 * scale
    c_core_radius = c_hole_radius - (1.5 * scale)
    c_rib_height = 5.0 * scale
    c_rib_flare_radius = c_hole_radius + (0.6 * scale)
    c_rib_base_radius = c_core_radius
    
    # Starts at the end of the bearing, points in -Z
    anchor_tip_z = -half_axle - flange_thickness - left_axle_pin_length
    l_anchor = Part.makeCylinder(c_core_radius, anchor_length, App.Vector(0,0,anchor_tip_z - anchor_length), App.Vector(0,0,1))
    
    curr_z = 0.0
    while curr_z + c_rib_height <= anchor_length:
        rib = Part.makeCone(c_rib_base_radius, c_rib_flare_radius, c_rib_height, App.Vector(0,0,anchor_tip_z - anchor_length + curr_z), App.Vector(0,0,1))
        l_anchor = l_anchor.fuse(rib)
        curr_z += c_rib_height
        
    tip_height = anchor_length - curr_z
    if tip_height > 0.01:
        tip_cone = Part.makeCone(c_rib_base_radius, c_rib_flare_radius, tip_height, App.Vector(0,0,anchor_tip_z - anchor_length + curr_z), App.Vector(0,0,1))
        l_anchor = l_anchor.fuse(tip_cone)

    l_pin = l_pin_bearing.fuse(l_anchor)
    for i in range(6):
        angle = math.radians(i * 60)
        hx = hole_dist * math.cos(angle)
        hy = hole_dist * math.sin(angle)
        cutter = Part.makeCylinder(hole_radius, flange_thickness + 10, App.Vector(hx, hy, -half_axle - flange_thickness - 5))
        l_flange = l_flange.cut(cutter)
        
    left_spool = l_flange.fuse(l_axle).fuse(l_pin).cut(l_axle_hole)
    return left_spool.removeSplitter()

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

    p_01_Spool_Left = build_left_spool()
    Part.show(p_01_Spool_Left, 'LeftSpool')
    print(f'Exporting 01_Spool_Left 1...')
    p_01_Spool_Left.exportStl(os.path.join(export_dir, '01_Spool_Left.stl'))
    p_01_Spool_Left.exportStep(os.path.join(export_dir, '01_Spool_Left.step'))
