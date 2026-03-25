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
    
    # 30% Axle length: Goes from Z=32 to Z=80 (48mm length)
    r_axle = Part.makeCylinder(axle_radius, 48 * scale, App.Vector(0,0, 32 * scale))
    
    def make_hex_prism(radius, length, placement):
        pts = []
        for i in range(7):
            angle = i * (math.pi / 3)
            pts.append(App.Vector(radius * math.cos(angle), radius * math.sin(angle), 0))
        face = Part.Face(Part.Wire(Part.makePolygon(pts)))
        prism = face.extrude(App.Vector(0, 0, length))
        prism.Placement = placement
        return prism

    clearance_amount = 0.4 * scale
    r_axle_peg = make_hex_prism(peg_radius - clearance_amount/2, 70 * scale, App.Placement(App.Vector(0,0,-37 * scale), App.Rotation(0,0,0,1)))
    
    # --- Center Bolt Through-Bore with Female Threads ---
    # Threading from Z=30 to beyond the handle peg (150mm length)
    t_pitch = 5.0 * scale
    t_radius = 12.0 * scale + clearance_amount  # Increased diameter
    t_start = -39.5 * scale
    t_length = 195.0 * scale
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
    t_core = Part.makeCylinder(t_r_inner, t_length + 20*scale, App.Vector(0,0,t_start - 10*scale))
    
    # Split cutter into core and sweep manually
    
    pin_base = App.Vector(0,0, half_axle + flange_thickness)
    r_pin = Part.makeCylinder(hub_hole_radius - clearance_amount, right_axle_pin_length, pin_base)
    
    # --- Hex Handle Peg & Anchor Tip ---
    handle_hex_len = handle_standoff + 10 * scale
    r_handle_hex = make_hex_prism(handle_peg_radius - clearance_amount/2, handle_hex_len, App.Placement(pin_base + App.Vector(0,0, right_axle_pin_length), App.Rotation(0,0,0,1)))
    r_handle_peg = r_handle_hex

    for i in range(6):
        angle = math.radians(i * 60)
        hx = hole_dist * math.cos(angle)
        hy = hole_dist * math.sin(angle)
        cutter = Part.makeCylinder(hole_radius, flange_thickness + 10, App.Vector(hx, hy, half_axle - 5))
        r_flange = r_flange.cut(cutter)

    right_spool = r_flange.fuse(r_axle).fuse(r_axle_peg).fuse(r_pin).fuse(r_handle_peg)
    
    
    thread_cutter = t_core.fuse(t_sweep).removeSplitter()
    right_spool = right_spool.cut(thread_cutter)
    
    return right_spool.removeSplitter()

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

    p_01_Spool_Right = build_right_spool()
    Part.show(p_01_Spool_Right, 'RightSpool')
    print(f'Exporting 01_Spool_Right...')
    p_01_Spool_Right.exportStl(os.path.join(export_dir, '01_Spool_Right.stl'))
    p_01_Spool_Right.exportStep(os.path.join(export_dir, '01_Spool_Right.step'))