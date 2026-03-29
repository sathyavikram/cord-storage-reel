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
import sys
if "params" in sys.modules: del sys.modules["params"]
from params import *

def build_caps():
    cap_thickness = 10 * scale
    cap_rad = hub_radius

    # We want a 5mm visual gap between the outside of the frame and the cap
    left_axle_pin_length = z_gap + hub_thickness + (5.0 * scale)
    anchor_tip_z = -half_axle - flange_thickness - left_axle_pin_length
    
    # Cap body
    cap_h = cap_thickness
    cap_L = Part.makeCylinder(cap_rad, cap_h, App.Vector(0,0, anchor_tip_z - cap_h))
    
    # Male Threaded Peg - Nominal dimensions, clearance handled in female socket
    t_pitch = 5.0 * scale
    t_radius = 25.0 * scale  # Nominal radius
    t_length = 24.0 * scale
    t_r_inner = 25.0 * scale - (t_pitch * 0.45)  # Nominal root radius
    
    t_helix = Part.makeHelix(t_pitch, t_length, t_r_inner, 0)
    
    inner_X = t_r_inner - 2.0 * scale
    p1 = App.Vector(inner_X, 0, -t_pitch*0.35)
    p2 = App.Vector(t_radius, 0, -t_pitch*0.1)
    p3 = App.Vector(t_radius, 0,  t_pitch*0.1)
    p4 = App.Vector(inner_X, 0,  t_pitch*0.35)
    t_wire = Part.Wire(Part.makePolygon([p1, p2, p3, p4, p1]))
    
    t_sweep = Part.Wire(t_helix).makePipeShell([t_wire], True, True)
    t_sweep.Placement = App.Placement(App.Vector(0,0,anchor_tip_z), App.Rotation(0,0,0,1))
    t_core = Part.makeCylinder(t_r_inner, t_length, App.Vector(0,0,anchor_tip_z))
    
    thread_peg = t_core.fuse(t_sweep)
    
    # Bevel tip
    bevel = Part.makeCone(t_radius + 2, t_r_inner, t_pitch/2 + 2, App.Vector(0,0,anchor_tip_z + t_length - t_pitch/2 - 2))
    thread_peg = thread_peg.cut(Part.makeCylinder(t_radius + 5, t_pitch + 2, App.Vector(0,0,anchor_tip_z + t_length - 2)).cut(bevel))

    cap_L = cap_L.fuse(thread_peg)

    # Flathead screwdriver slot for grip
    slot_width = 3.0 * scale
    slot_length = cap_rad * 2 + 1.0
    slot_depth = 4.0 * scale
    slot = Part.makeBox(slot_length, slot_width, slot_depth, 
                        App.Vector(-slot_length/2, -slot_width/2, anchor_tip_z - cap_h - 0.1))
    cap_L = cap_L.cut(slot)

    export_dir = EXPORT_DIR
    os.makedirs(export_dir, exist_ok=True)
    stl_file = os.path.join(export_dir, 'part_05_caps.stl')
    step_file = os.path.join(export_dir, 'part_05_caps.step')
    for f_path in [stl_file, step_file]:
        if os.path.exists(f_path):
            os.remove(f_path)
    print(f'Exporting part_05_caps...')
    cap_L.exportStl(stl_file)
    cap_L.exportStep(step_file)

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

    parts = build_caps()
    if parts[0] is not None:
        pass
        
    if parts[1] is not None:
        Part.show(parts[1], 'CapLeft')