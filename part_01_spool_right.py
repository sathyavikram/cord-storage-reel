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

def build_right_spool():
    r_flange = Part.makeCylinder(flange_radius, flange_thickness, App.Vector(0,0, half_axle))
    
    # 50% Axle length: perfectly centered joint
    r_axle = Part.makeCylinder(axle_radius, half_axle, App.Vector(0,0, 0))
    
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
    hex_len = 45.0 * scale
    r_axle_peg = make_hex_prism(peg_radius - clearance_amount/2, hex_len, App.Placement(App.Vector(0,0,-hex_len), App.Rotation(0,0,0,1)))
    
    # --- Threading just for the Handle Bolt ---
    # Threading from top of the handle peg down a bit (~45mm total depth)
    t_pitch = 5.0 * scale
    t_radius = 12.0 * scale + clearance_amount  # Increased diameter
    desired_t_start = right_frame_outer_z - 35.0 * scale
    t_start = round(desired_t_start / t_pitch) * t_pitch
    t_length = 65.0 * scale + (desired_t_start - t_start)
    t_r_inner = 12.0 * scale - (t_pitch * 0.45) + clearance_amount

    t_helix = Part.makeHelix(t_pitch, t_length, t_r_inner, 0)
    
    inner_X = t_r_inner - 2.0 * scale
    p1 = App.Vector(inner_X, 0, -t_pitch*0.35)
    p2 = App.Vector(t_radius, 0, -t_pitch*0.1)
    p3 = App.Vector(t_radius, 0,  t_pitch*0.1)
    p4 = App.Vector(inner_X, 0,  t_pitch*0.35)
    t_wire = Part.Wire(Part.makePolygon([p1, p2, p3, p4, p1]))
    
    t_sweep = Part.Wire(t_helix).makePipeShell([t_wire], True, True)
    t_sweep.Placement = App.Placement(App.Vector(0,0,t_start), App.Rotation(0,0,0,1))
    t_core = Part.makeCylinder(t_r_inner, t_length + 20*scale, App.Vector(0,0,t_start - 10*scale))
    
    # Split cutter into core and sweep manually
    
    pin_base = App.Vector(0,0, half_axle + flange_thickness)
    r_pin = Part.makeCylinder(pin_radius, right_axle_pin_length, pin_base)
    
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
    
    part = right_spool.removeSplitter()
    
    export_dir = EXPORT_DIR
    os.makedirs(export_dir, exist_ok=True)
    stl_file = os.path.join(export_dir, 'part_01_spool_right.stl')
    step_file = os.path.join(export_dir, 'part_01_spool_right.step')
    for f_path in [stl_file, step_file]:
        if os.path.exists(f_path):
            os.remove(f_path)
    print(f'Exporting part_01_spool_right...')
    part.exportStl(stl_file)
    part.exportStep(step_file)
    
    return part

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

    p_01_Spool_Right = build_right_spool()
    Part.show(p_01_Spool_Right, 'RightSpool')