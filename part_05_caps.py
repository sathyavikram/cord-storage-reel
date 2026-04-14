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
    cap_thickness = cap_depth
    cap_rad = 36.0 * scale

    # Build the cap at origin
    anchor_z = 0.0
    
    # Cap body
    cap_h = cap_thickness
    cap_L = Part.makeCylinder(cap_rad, cap_h, App.Vector(0,0, anchor_z - cap_h))
    
    # Male Threaded Peg - Nominal dimensions, clearance handled in female socket
    t_pitch = 5.0 * scale
    
    # Shrink the entire cap thread radius to add extra clearance for easy rotation.
    extra_clearance = 0.6 * scale
    t_radius = (12.0 * scale) - extra_clearance  # Nominal radius is 12
    
    t_length = 60.0 * scale
    t_r_inner = t_radius - (t_pitch * 0.45)  # Nominal root radius
    
    t_helix = Part.makeHelix(t_pitch, t_length, t_r_inner, 0)
    
    inner_X = t_r_inner - 2.0 * scale
    p1 = App.Vector(inner_X, 0, -t_pitch*0.35)
    p2 = App.Vector(t_radius, 0, -t_pitch*0.1)
    p3 = App.Vector(t_radius, 0,  t_pitch*0.1)
    p4 = App.Vector(inner_X, 0,  t_pitch*0.35)
    t_wire = Part.Wire(Part.makePolygon([p1, p2, p3, p4, p1]))
    
    t_sweep = Part.Wire(t_helix).makePipeShell([t_wire], True, True)
    t_sweep.Placement = App.Placement(App.Vector(0,0,anchor_z), App.Rotation(0,0,0,1))
    
    # Extend core down to capture the floating down-curling sweep
    core_ext = t_pitch
    t_core = Part.makeCylinder(t_r_inner, t_length, App.Vector(0,0,anchor_z))
    t_core_ext = Part.makeCylinder(t_r_inner, core_ext, App.Vector(0,0,anchor_z - core_ext))
    t_core = t_core.fuse(t_core_ext)

    # Flathead screwdriver slot for grip
    slot_width = 3.0 * scale
    slot_length = cap_rad * 2 + 1.0
    slot_depth = 4.0 * scale
    slot = Part.makeBox(slot_length, slot_width, slot_depth, 
                        App.Vector(-slot_length/2, -slot_width/2, anchor_z - cap_h - 0.1))
    cap_L = cap_L.cut(slot)
    
    # Avoid OpenCASCADE boolean hangs by using makeCompound for the final 3D printing export
    # The overlapping shapes (head, core, and thread sweep) slice perfectly in Bambu/PrusaSlicer
    cap_final = Part.makeCompound([cap_L, t_core, t_sweep])

    export_dir = EXPORT_DIR
    os.makedirs(export_dir, exist_ok=True)
    stl_file = os.path.join(export_dir, 'part_05_caps.stl')
    step_file = os.path.join(export_dir, 'part_05_caps.step')
    for f_path in [stl_file, step_file]:
        if os.path.exists(f_path):
            os.remove(f_path)
    print(f'Exporting part_05_caps...')
    cap_final.exportStl(stl_file)
    cap_final.exportStep(step_file)

    return None, cap_final

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