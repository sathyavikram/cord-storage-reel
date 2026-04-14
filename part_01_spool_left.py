import sys, os
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
import math
import sys
if "params" in sys.modules: del sys.modules["params"]
from params import *

def build_left_spool():
    l_flange = Part.makeCylinder(flange_radius, flange_thickness, App.Vector(0,0, -half_axle - flange_thickness))
    # 50% Axle length: perfectly centered joint
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
    clearance_amount = 0.4 * scale
    hex_depth = 50.0 * scale
    l_axle_hole = make_hex_prism(peg_radius + clearance_amount, hex_depth, App.Placement(App.Vector(0,0,-hex_depth + 1.0 * scale), App.Rotation(0,0,0,1)))

    left_axle_pin_length = z_gap + hub_thickness + (5.0 * scale)
    l_pin_bearing = Part.makeCylinder(pin_radius, left_axle_pin_length, App.Vector(0,0, -half_axle - flange_thickness - left_axle_pin_length))

    # Left Outer Cap Socket (Female Thread) - Extended to cut through flange and axle
    anchor_tip_z = -half_axle - flange_thickness - left_axle_pin_length
    
    c_pitch = 5.0 * scale
    c_radius = 12.0 * scale + clearance_amount  # Match universal cap radius
    c_length = 65.0 * scale  # Extended length to accommodate Universal Cap thread
    c_r_inner = 12.0 * scale - (c_pitch * 0.45) + clearance_amount
    
    c_helix = Part.makeHelix(c_pitch, c_length, c_r_inner, 0)
    
    inner_X = c_r_inner - 2.0 * scale
    p1 = App.Vector(inner_X, 0, -c_pitch*0.35)
    p2 = App.Vector(c_radius, 0, -c_pitch*0.1)
    p3 = App.Vector(c_radius, 0,  c_pitch*0.1)
    p4 = App.Vector(inner_X, 0,  c_pitch*0.35)
    c_wire = Part.Wire(Part.makePolygon([p1, p2, p3, p4, p1]))
    
    c_sweep = Part.Wire(c_helix).makePipeShell([c_wire], True, True)
    c_sweep.Placement = App.Placement(App.Vector(0,0,anchor_tip_z - 1.0), App.Rotation(0,0,0,1))
    c_core = Part.makeCylinder(c_r_inner, c_length, App.Vector(0,0,anchor_tip_z - 1.0))
    
    chamfer = Part.makeCone(c_radius + 4, c_r_inner, c_pitch/2 + 4, App.Vector(0,0,anchor_tip_z - 2.0))

    for i in range(1, 6):
        angle = math.radians(i * 60)
        hx = hole_dist * math.cos(angle)
        hy = hole_dist * math.sin(angle)
        cutter = Part.makeCylinder(hole_radius, flange_thickness + 10, App.Vector(hx, hy, -half_axle - flange_thickness - 5))
        l_flange = l_flange.cut(cutter)
    
    # --- Side-Wall Slot for Plug/Wire Retainer ---
    # Placed over the solid flange area (where the hole was skipped, angle = 0)
    ret_x = hole_dist + 5.0 * scale
    ret_y = 0
    ret_z = -half_axle
    ret_l = 40.0 # Force absolute 40mm length (30mm cavity + 10mm inner wall)
    ret_w = (30.0 / scale) + (13.0 * scale) # ensure outer block can fit the 30mm unscaled cavity 
    ret_h = 25.0 # absolute 25mm height
    
    retainer = Part.makeBox(ret_l, ret_w, ret_h, App.Vector(ret_x - ret_l/2, ret_y - ret_w/2, ret_z))
    
    # Wire slot: straight channel along X, 10mm absolute width for cord
    wire_slot_w = 10.0 # Force absolute 10mm width regardless of scale
    wire_slot = Part.makeBox(ret_l + 5, wire_slot_w, ret_h + 5, App.Vector(ret_x - ret_l/2 - 2.5, ret_y - wire_slot_w/2, ret_z - 2.5))
    
    # Plug cavity: wider section on the outer side for the male/female plug body
    plug_cavity_w = 30.0 # Force absolute 30mm width regardless of global scale
    plug_cavity_l = 30.0 # Force absolute 30mm length regardless of global scale
    plug_cavity = Part.makeBox(plug_cavity_l + 5, plug_cavity_w, ret_h + 5, App.Vector(ret_x + ret_l/2 - plug_cavity_l, ret_y - plug_cavity_w/2, ret_z - 2.5))
    
    # Top snap lips to keep cord from jumping out
    lip_w = 2.0 * scale
    lip1 = Part.makeBox(ret_l + 5, lip_w, 3.0 * scale, App.Vector(ret_x - ret_l/2 - 2.5, ret_y - wire_slot_w/2, ret_z + ret_h - 3.0 * scale))
    lip2 = Part.makeBox(ret_l + 5, lip_w, 3.0 * scale, App.Vector(ret_x - ret_l/2 - 2.5, ret_y + wire_slot_w/2 - lip_w, ret_z + ret_h - 3.0 * scale))
    
    retainer = retainer.cut(wire_slot).cut(plug_cavity)
    # Add snap lips across the top of the channel
    retainer = retainer.fuse(lip1).fuse(lip2)
    # Clean up any bits of lip that protrude into the plug cavity
    retainer = retainer.cut(plug_cavity)
    
    # Fillet all edges of the retainer/slot object
    try:
        # We try to fillet all edges with a 1.0mm radius. 
        # (Excluding the bottom face edges is ideal, but FreeCAD will usually handle it well enough if fused later)
        fillet_radius = 1.0
        retainer = retainer.makeFillet(fillet_radius, retainer.Edges)
    except Exception as e:
        print(f"Warning: Retainer fillet failed: {e}")

    
    # --- Add Strength Ribs/Gussets ---
    rib_thickness = 4.0 * scale
    rib_height = 20.0 * scale
    rib_length = 35.0 * scale
    
    rib_wire = Part.Wire(Part.makePolygon([
        App.Vector(axle_radius - 7, 0, -half_axle),
        App.Vector(axle_radius - 7, 0, -half_axle + rib_height),
        App.Vector(axle_radius - 1 + rib_length, 0, -half_axle),
        App.Vector(axle_radius - 7, 0, -half_axle)
    ]))
    rib_face = Part.Face(rib_wire)
    rib_solid = rib_face.extrude(App.Vector(0, rib_thickness, 0))
    rib_solid.translate(App.Vector(0, -rib_thickness/2.0, 0))
    
    ribs = []
    for i in range(6):
        # We need to offset the angle by 30 degrees so ribs fall BETWEEN the holes
        angle = math.radians(i * 60 + 30)
        rib = rib_solid.copy()
        rib.rotate(App.Vector(0,0,0), App.Vector(0,0,1), math.degrees(angle))
        ribs.append(rib)
    
    # 1. Fuse basic geometry and ribs
    left_spool = l_flange.fuse(l_axle).fuse(l_pin_bearing).fuse(retainer)
    print("V1 base:", left_spool.Volume)
    for r in ribs:
        left_spool = left_spool.fuse(r)
    print("V2 ribs:", left_spool.Volume)
        
    # 2. Cut internal holes sequentially (no complex multi-part cutters)
    left_spool = left_spool.cut(l_axle_hole)
    print("V3 ax_hole:", left_spool.Volume)
    
    left_spool = left_spool.cut(c_core)
    print("V4 c_core:", left_spool.Volume)
    
    left_spool = left_spool.cut(c_sweep)
    print("V5 c_sweep:", left_spool.Volume)
    
    left_spool = left_spool.cut(chamfer)
    print("V6 chamfer:", left_spool.Volume)
    
    left_spool = left_spool.removeSplitter()
    print("V7 removeSplitter:", left_spool.Volume)
    
    export_dir = EXPORT_DIR
    os.makedirs(export_dir, exist_ok=True)
    stl_file = os.path.join(export_dir, 'part_01_spool_left.stl')
    step_file = os.path.join(export_dir, 'part_01_spool_left.step')
    for f_path in [stl_file, step_file]:
        if os.path.exists(f_path):
            os.remove(f_path)
    print(f'Exporting part_01_spool_left...')
    left_spool.exportStl(stl_file)
    left_spool.exportStep(step_file)
    
    return left_spool

if __name__ == '__main__':
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

    p_01_Spool_Left = build_left_spool()
    Part.show(p_01_Spool_Left, 'LeftSpool')
