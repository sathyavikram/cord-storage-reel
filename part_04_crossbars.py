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
    nest_depth = 5.0 * scale
    anchor_length = 20.0 * scale
    
    # Inner face boundaries
    inner_L = z_L + hub_thickness/2
    inner_R = z_R - hub_thickness/2
    
    # Ends of the main crossbar cylinder (it enters the nest)
    start_z = inner_L - nest_depth
    end_z = inner_R + nest_depth
    bar_len = end_z - start_z
    
    # Pin parameters
    hole_radius = 9.0 * scale
    core_radius = hole_radius - (1.5 * scale)
    rib_height = 5.0 * scale
    rib_flare_radius = hole_radius + (0.6 * scale)
    rib_base_radius = core_radius

    # Cutter (now it's an additive pin pointing +Z)
    pin_L = Part.makeCylinder(core_radius, anchor_length, App.Vector(0,0,0), App.Vector(0,0,1))
    current_z = 0.0
    while current_z + rib_height <= anchor_length:
        rib = Part.makeCone(rib_flare_radius, rib_base_radius, rib_height, App.Vector(0,0,current_z), App.Vector(0,0,1))
        pin_L = pin_L.fuse(rib)
        current_z += rib_height
        
    tip_height = anchor_length - current_z
    if tip_height > 0.01:
        tip_cone = Part.makeCone(rib_flare_radius, core_radius - (1.0*scale), tip_height, App.Vector(0,0,current_z), App.Vector(0,0,1))
        pin_L = pin_L.fuse(tip_cone)

    # Cut compliance slots
    cut_w = 2.0 * scale
    cut_h = anchor_length + 2.0 * scale
    box_s = 40.0 * scale
    c1 = Part.makeBox(box_s, cut_w, cut_h, App.Vector(-box_s/2, -cut_w/2, -1.0 * scale))
    c2 = Part.makeBox(cut_w, box_s, cut_h, App.Vector(-cut_w/2, -box_s/2, -1.0 * scale))
    pin_L = pin_L.cut(c1).cut(c2)

    base_pin = pin_L
    
    def make_crossbar(pos_x, pos_y):
        # The main bar body (including nest depth)
        bar = Part.makeCylinder(crossbar_radius, bar_len, App.Vector(pos_x, pos_y, start_z))
        
        # Left Pin (pointing -Z from start_z)
        pL = base_pin.copy()
        pL.Placement = App.Placement(App.Vector(pos_x, pos_y, start_z), App.Rotation(App.Vector(1,0,0), 180)) # Rotated 180 on X to point -Z
        
        # Right Pin (pointing +Z from end_z)
        pR = base_pin.copy()
        pR.Placement = App.Placement(App.Vector(pos_x, pos_y, end_z), App.Rotation(0,0,0,1))
        
        return bar.fuse(pL).fuse(pR).removeSplitter()

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
