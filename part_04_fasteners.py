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

def build_fastener():
    t_pitch = 4.0 * scale
    
    # Shrink the fastener thread radius to add extra clearance for easy rotation.
    extra_clearance = 0.4 * scale
    t_radius = (8.0 * scale) - extra_clearance
    
    thread_length = 25.0 * scale
    smooth_length = 5.0 * scale
    head_height = 6.0 * scale  # Counterbore is 6.5
    head_radius = 13.5 * scale # Counterbore is 14.0
    
    t_r_inner = t_radius - (t_pitch * 0.45)
    
    # 1. The Head (printed flat on bed at Z=0)
    head = Part.makeCylinder(head_radius, head_height, App.Vector(0,0,0))
    
    # Flathead screwdriver slot
    slot_width = 3.0 * scale
    slot_length = head_radius * 2 + 1.0
    slot_depth = 3.0 * scale
    slot = Part.makeBox(slot_length, slot_width, slot_depth, App.Vector(-slot_length/2, -slot_width/2, -0.1))
    head = head.cut(slot)
    
    # 2. Smooth shaft
    shaft_start = head_height
    smooth = Part.makeCylinder(t_radius, smooth_length, App.Vector(0,0,shaft_start))
    
    # 3. Threaded shaft
    thread_start = shaft_start + smooth_length
    
    inner_X = t_r_inner - 1.0 * scale
    p1 = App.Vector(inner_X, 0, -t_pitch*0.35)
    p2 = App.Vector(t_radius - 0.2*scale, 0, -t_pitch*0.1) # Add tiny thread chamfer to smooth peaks
    p3 = App.Vector(t_radius - 0.2*scale, 0,  t_pitch*0.1)
    p4 = App.Vector(inner_X, 0,  t_pitch*0.35)
    t_wire = Part.Wire(Part.makePolygon([p1, p2, p3, p4, p1]))
    
    t_helix = Part.makeHelix(t_pitch, thread_length, t_r_inner, 0)
    t_sweep = Part.Wire(t_helix).makePipeShell([t_wire], True, True)
    t_sweep.Placement = App.Placement(App.Vector(0,0,thread_start), App.Rotation(0,0,0,1))
    
    t_core = Part.makeCylinder(t_r_inner, thread_length, App.Vector(0,0,thread_start))
    
    thread_part = t_core.fuse(t_sweep)
    
    # Bevel tip
    chamfer = Part.makeCone(t_radius + 2.0, t_r_inner, t_pitch/2 + 1, App.Vector(0,0,thread_start + thread_length - t_pitch/2 - 1))
    cutter = Part.makeCylinder(t_radius + 5.0, t_pitch + 2.0, App.Vector(0,0,thread_start + thread_length - 1))
    thread_part = thread_part.cut(cutter.cut(chamfer))

    bolt = head.fuse(smooth).fuse(thread_part).removeSplitter()
    
    export_dir = EXPORT_DIR
    os.makedirs(export_dir, exist_ok=True)
    stl_file = os.path.join(export_dir, 'part_04_fasteners.stl')
    step_file = os.path.join(export_dir, 'part_04_fasteners.step')
    for f_path in [stl_file, step_file]:
        if os.path.exists(f_path):
            os.remove(f_path)
    print(f'Exporting part_04_fasteners...')
    bolt.exportStl(stl_file)
    bolt.exportStep(step_file)
    
    return bolt

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

    bolt = build_fastener()
    Part.show(bolt, 'FrameBolt')