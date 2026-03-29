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

def build_crossbars_export():
    nest_depth = 8.0 * scale
    inner_L = z_L + hub_thickness/2
    inner_R = z_R - hub_thickness/2
    start_z = inner_L - nest_depth
    end_z = inner_R + nest_depth
    bar_len = end_z - start_z
    
    t_pitch = 4.0 * scale
    t_radius = 8.0 * scale + 0.4 * scale
    t_length = 35.0 * scale
    t_r_inner = 8.0 * scale - (t_pitch * 0.45) + 0.4 * scale

    inner_X = t_r_inner - 2.0 * scale
    p1 = App.Vector(inner_X, 0, -t_pitch*0.35)
    p2 = App.Vector(t_radius, 0, -t_pitch*0.1)
    p3 = App.Vector(t_radius, 0,  t_pitch*0.1)
    p4 = App.Vector(inner_X, 0,  t_pitch*0.35)
    t_wire = Part.Wire(Part.makePolygon([p1, p2, p3, p4, p1]))
    
    t_helix = Part.makeHelix(t_pitch, t_length, t_r_inner, 0)
    t_sweep = Part.Wire(t_helix).makePipeShell([t_wire], True, True)
    t_core = Part.makeCylinder(t_r_inner, t_length, App.Vector(0,0,0))
    thread_cutter = t_core.fuse(t_sweep)
    
    chamfer = Part.makeCone(t_radius + 2.0, t_r_inner, t_pitch, App.Vector(0,0,0))
    thread_cutter = thread_cutter.fuse(chamfer)
    
    tip_bore = Part.makeCylinder(t_r_inner, 5.0 * scale, App.Vector(0,0,t_length-5.0*scale))
    thread_cutter = thread_cutter.fuse(tip_bore)

    bar = Part.makeCylinder(crossbar_radius, bar_len, App.Vector(0, 0, start_z))
    cutL = thread_cutter.copy()
    cutL.Placement = App.Placement(App.Vector(0, 0, start_z - 1.0), App.Rotation(0,0,0,1))
    cutR = thread_cutter.copy()
    cutR.Placement = App.Placement(App.Vector(0, 0, end_z + 1.0), App.Rotation(App.Vector(1,0,0), 180))
    bar = bar.cut(cutL).cut(cutR).removeSplitter()
    
    export_dir = EXPORT_DIR
    os.makedirs(export_dir, exist_ok=True)
    
    stl_file = os.path.join(export_dir, 'part_04_crossbars.stl')
    step_file = os.path.join(export_dir, 'part_04_crossbars.step')
    for f_path in [stl_file, step_file]:
        if os.path.exists(f_path):
            os.remove(f_path)
    print(f'Exporting part_04_crossbars...')
    bar.exportStl(stl_file)
    bar.exportStep(step_file)
    
    return bar

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

    part = build_crossbars_export()
    Part.show(part, 'Crossbar')
