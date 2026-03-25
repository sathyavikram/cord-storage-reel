import sys, os
try:
    _script_dir = os.path.dirname(os.path.abspath(__file__))
except NameError:
    _script_dir = os.getcwd()
if _script_dir not in sys.path:
    sys.path.insert(0, _script_dir)
import FreeCAD as App
import Part
import sys
if "params" in sys.modules: del sys.modules["params"]
from params import *

def build_crossbars():
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

    def make_crossbar(pos_x, pos_y):
        bar = Part.makeCylinder(crossbar_radius, bar_len, App.Vector(pos_x, pos_y, start_z))
        
        cutL = thread_cutter.copy()
        cutL.Placement = App.Placement(App.Vector(pos_x, pos_y, start_z - 1.0), App.Rotation(0,0,0,1))
        
        cutR = thread_cutter.copy()
        cutR.Placement = App.Placement(App.Vector(pos_x, pos_y, end_z + 1.0), App.Rotation(App.Vector(1,0,0), 180))
        
        return bar.cut(cutL).cut(cutR).removeSplitter()

    bar1 = make_crossbar(x_spread, y_floor)
    bar2 = make_crossbar(-x_spread, y_floor)
    bar3 = make_crossbar(0, y_top)
    
    return bar1, bar2, bar3

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

    parts = build_crossbars()
    Part.show(parts[0], 'CrossbarFront')
    print(f'Exporting 04_Crossbar_Front...')
    parts[0].exportStl(os.path.join(export_dir, '04_Crossbar_Front.stl'))
    parts[0].exportStep(os.path.join(export_dir, '04_Crossbar_Front.step'))
    Part.show(parts[1], 'CrossbarBack')
    print(f'Exporting 04_Crossbar_Back...')
    parts[1].exportStl(os.path.join(export_dir, '04_Crossbar_Back.stl'))
    parts[1].exportStep(os.path.join(export_dir, '04_Crossbar_Back.step'))
    Part.show(parts[2], 'CrossbarTop')
    print(f'Exporting 04_Crossbar_Top...')
    parts[2].exportStl(os.path.join(export_dir, '04_Crossbar_Top.stl'))
    parts[2].exportStep(os.path.join(export_dir, '04_Crossbar_Top.step'))
