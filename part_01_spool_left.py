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
    
    cap_cutter = c_core.fuse(c_sweep)
    
    chamfer = Part.makeCone(c_radius + 4, c_r_inner, c_pitch/2 + 4, App.Vector(0,0,anchor_tip_z - 2.0))
    cap_cutter = cap_cutter.fuse(chamfer)

    for i in range(6):
        angle = math.radians(i * 60)
        hx = hole_dist * math.cos(angle)
        hy = hole_dist * math.sin(angle)
        cutter = Part.makeCylinder(hole_radius, flange_thickness + 10, App.Vector(hx, hy, -half_axle - flange_thickness - 5))
        l_flange = l_flange.cut(cutter)
    
    # Build spool and cut cap socket through all components (flange, axle, pin)
    
    left_spool = l_flange.fuse(l_axle).fuse(l_pin_bearing)
    
    left_spool = left_spool.cut(l_axle_hole)
    
    # Actually cut the cap threaded hole from the spool
    left_spool = left_spool.cut(cap_cutter)
    left_spool = left_spool.removeSplitter()
    
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
