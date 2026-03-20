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

def build_frame(z_plane):
    P_hub = App.Vector(0, 0, z_plane)
    P_f = App.Vector(x_spread, y_floor, z_plane)
    P_b = App.Vector(-x_spread, y_floor, z_plane)
    P_t = App.Vector(0, y_top, z_plane)

    def make_strut(p1, p2):
        v = p2 - p1
        L = v.Length
        box = Part.makeBox(L, frame_width, hub_thickness, App.Vector(0, -frame_width/2, -hub_thickness/2))
        c1 = Part.makeCylinder(frame_width/2, hub_thickness, App.Vector(0,0,-hub_thickness/2))
        c2 = Part.makeCylinder(frame_width/2, hub_thickness, App.Vector(L,0,-hub_thickness/2))
        strut = box.fuse(c1).fuse(c2)
        angle = math.degrees(math.atan2(v.y, v.x))
        strut.Placement = App.Placement(p1, App.Rotation(App.Vector(0,0,1), angle))
        return strut

    s1 = make_strut(P_hub, P_f)
    s2 = make_strut(P_hub, P_b)
    s3 = make_strut(P_f, P_b)
    s4 = make_strut(P_hub, P_t)
    ring = Part.makeCylinder(hub_radius, hub_thickness, P_hub - App.Vector(0,0,hub_thickness/2))
    frame = s1.fuse(s2).fuse(s3).fuse(s4).fuse(ring)
    
    hole = Part.makeCylinder(hub_hole_radius, hub_thickness + 10, P_hub - App.Vector(0,0,hub_thickness/2 + 5))
    
    sock1 = Part.makeCylinder(crossbar_radius + clearance, hub_thickness + 10, P_f - App.Vector(0,0,hub_thickness/2 + 5))
    sock2 = Part.makeCylinder(crossbar_radius + clearance, hub_thickness + 10, P_b - App.Vector(0,0,hub_thickness/2 + 5))
    sock3 = Part.makeCylinder(crossbar_radius + clearance, hub_thickness + 10, P_t - App.Vector(0,0,hub_thickness/2 + 5))
    
    return frame.cut(hole).cut(sock1).cut(sock2).cut(sock3).removeSplitter()

def build_right_frame():
    return build_frame(z_R)

def build_left_frame():
    return build_frame(z_L)

if __name__ == '__main__':
    import FreeCAD as App
    import Part
    import os

    doc_name = "Doc_" + os.path.basename(__file__).replace(".py", "")
    doc = App.newDocument(doc_name)

    export_dir = EXPORT_DIR
    os.makedirs(export_dir, exist_ok=True)

    p_03_Frame_Right = build_right_frame()
    Part.show(p_03_Frame_Right, 'RightFrame')
    print(f'Exporting 03_Frame_Right...')
    p_03_Frame_Right.exportStl(os.path.join(export_dir, '03_Frame_Right.stl'))
    p_03_Frame_Right.exportStep(os.path.join(export_dir, '03_Frame_Right.step'))
    p_03_Frame_Left = build_left_frame()
    Part.show(p_03_Frame_Left, 'LeftFrame')
    print(f'Exporting 03_Frame_Left...')
    p_03_Frame_Left.exportStl(os.path.join(export_dir, '03_Frame_Left.stl'))
    p_03_Frame_Left.exportStep(os.path.join(export_dir, '03_Frame_Left.step'))
