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
    # 70% Axle length: Goes from Z=-80 to Z=32 (112mm total)
    l_axle = Part.makeCylinder(axle_radius, 112 * scale, App.Vector(0,0,-half_axle))

    def make_hex_prism(radius, length, placement):
        pts = []
        for i in range(7):
            angle = i * (math.pi / 3)
            pts.append(App.Vector(radius * math.cos(angle), radius * math.sin(angle), 0))
        face = Part.Face(Part.Wire(Part.makePolygon(pts)))
        prism = face.extrude(App.Vector(0, 0, length))
        prism.Placement = placement
        return prism

    # The main hex receiver hole (from Z=31 to Z=55)
    clearance_amount = 0.4 * scale
    l_axle_hole = make_hex_prism(peg_radius + clearance_amount, 58.0*scale, App.Placement(App.Vector(0,0,-24.5*scale), App.Rotation(0,0,0,1)))

    # --- Internal Thread Cutter for Center Bolt ---
    # Threading the inner bore from Z=5 to Z=55 (50mm length)
    t_pitch = 5.0 * scale
    t_radius = 12.0 * scale + clearance_amount  # Increased diameter
    desired_t_start = -78.0 * scale
    t_start = round(desired_t_start / t_pitch) * t_pitch
    t_length = 60.0 * scale + (desired_t_start - t_start + 10*scale)
    t_r_inner = 12.0 * scale - (t_pitch * 0.45) + clearance_amount
    
    t_helix = Part.makeHelix(t_pitch, t_length, t_r_inner, 0)
    t_helix.Placement = App.Placement(App.Vector(0,0,t_start), App.Rotation(0,0,0,1))
    
    inner_X = t_r_inner - 2.0 * scale
    p1 = App.Vector(inner_X, 0, -t_pitch*0.35 + t_start)
    p2 = App.Vector(t_radius, 0, -t_pitch*0.1 + t_start)
    p3 = App.Vector(t_radius, 0,  t_pitch*0.1 + t_start)
    p4 = App.Vector(inner_X, 0,  t_pitch*0.35 + t_start)
    t_wire = Part.Wire(Part.makePolygon([p1, p2, p3, p4, p1]))
    
    t_sweep = Part.Wire(t_helix).makePipeShell([t_wire], True, True)
    t_core = Part.makeCylinder(t_r_inner, t_length + 25.0 * scale, App.Vector(0, 0, t_start - 25.0 * scale))
    
    thread_cutter = t_core.fuse(t_sweep)
    
    # Optional chamfer for the thread entrance to help align the bolt at Z=55
    
    

    

    # Allow space for the bolt tip extending further if necessary
    
    

    left_axle_pin_length = z_gap + hub_thickness + (5.0 * scale)
    l_pin_bearing = Part.makeCylinder(pin_radius, left_axle_pin_length, App.Vector(0,0, -half_axle - flange_thickness - left_axle_pin_length))

    # Left Outer Cap Socket (Female Thread) - Extended to cut through flange and axle
    anchor_tip_z = -half_axle - flange_thickness - left_axle_pin_length
    
    c_pitch = 5.0 * scale
    c_radius = 25.0 * scale + clearance_amount  # Increased diameter for better cut
    c_length = 40.0 * scale  # Extended length to cut through flange (15mm) and into axle
    c_r_inner = 25.0 * scale - (c_pitch * 0.45) + clearance_amount
    
    c_helix = Part.makeHelix(c_pitch, c_length, c_r_inner, 0)
    c_helix.Placement = App.Placement(App.Vector(0,0,anchor_tip_z - 1.0), App.Rotation(0,0,0,1))
    
    inner_X = c_r_inner - 2.0 * scale
    p1 = App.Vector(inner_X, 0, -c_pitch*0.35 + anchor_tip_z - 1.0)
    p2 = App.Vector(c_radius, 0, -c_pitch*0.1 + anchor_tip_z - 1.0)
    p3 = App.Vector(c_radius, 0,  c_pitch*0.1 + anchor_tip_z - 1.0)
    p4 = App.Vector(inner_X, 0,  c_pitch*0.35 + anchor_tip_z - 1.0)
    c_wire = Part.Wire(Part.makePolygon([p1, p2, p3, p4, p1]))
    
    c_sweep = Part.Wire(c_helix).makePipeShell([c_wire], True, True)
    c_core = Part.makeCylinder(c_r_inner, c_length, App.Vector(0,0,anchor_tip_z - 1.0))
    
    cap_cutter = c_core.fuse(c_sweep)
    
    chamfer = Part.makeCone(c_radius + 2, c_r_inner, c_pitch/2 + 2, App.Vector(0,0,anchor_tip_z))
    cap_cutter = cap_cutter.fuse(chamfer)

    for i in range(6):
        angle = math.radians(i * 60)
        hx = hole_dist * math.cos(angle)
        hy = hole_dist * math.sin(angle)
        cutter = Part.makeCylinder(hole_radius, flange_thickness + 10, App.Vector(hx, hy, -half_axle - flange_thickness - 5))
        l_flange = l_flange.cut(cutter)
    
    # Build spool and cut cap socket through all components (flange, axle, pin)
    
    left_spool = l_flange.fuse(l_axle).fuse(l_pin_bearing)
    
    # Unified thread cutter
    thread_cutter = t_core.fuse(t_sweep).removeSplitter()
    
    # Cap cutter
    cap_cutter = cap_cutter.removeSplitter()
    
    left_spool = left_spool.cut(l_axle_hole)
    left_spool = left_spool.cut(thread_cutter)
    left_spool = left_spool.cut(cap_cutter)
    
    return left_spool.removeSplitter()
    
    # Cap cutter
    cap_cutter = cap_cutter.removeSplitter()
    
    left_spool = left_spool.cut(l_axle_hole)
    left_spool = left_spool.cut(thread_cutter)
    left_spool = left_spool.cut(cap_cutter)
    
    return left_spool.removeSplitter()

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

    export_dir = EXPORT_DIR
    os.makedirs(export_dir, exist_ok=True)

    p_01_Spool_Left = build_left_spool()
    Part.show(p_01_Spool_Left, 'LeftSpool')
    print(f'Exporting 01_Spool_Left...')
    p_01_Spool_Left.exportStl(os.path.join(export_dir, '01_Spool_Left.stl'))
    p_01_Spool_Left.exportStep(os.path.join(export_dir, '01_Spool_Left.step'))