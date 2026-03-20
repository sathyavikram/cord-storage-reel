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
    bar_len = (z_R + hub_thickness/2) - (z_L - hub_thickness/2)
    z_origin = z_L - hub_thickness/2

    bar1 = Part.makeCylinder(crossbar_radius, bar_len, App.Vector(x_spread, y_floor, z_origin))
    bar2 = Part.makeCylinder(crossbar_radius, bar_len, App.Vector(-x_spread, y_floor, z_origin))
    bar3 = Part.makeCylinder(crossbar_radius, bar_len, App.Vector(0, y_top, z_origin))
    
    return bar1, bar2, bar3

if __name__ == '__main__':
    import FreeCAD as App
    import Part
    import os

    doc_name = "Doc_" + os.path.basename(__file__).replace(".py", "")
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
