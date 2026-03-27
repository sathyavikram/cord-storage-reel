import FreeCAD as App
import Part
import math
import os
import sys

try:
    _script_dir = os.path.dirname(os.path.abspath(__file__))
except NameError:
    _script_dir = os.getcwd()
if _script_dir not in sys.path:
    sys.path.insert(0, _script_dir)

if "params" in sys.modules: del sys.modules["params"]
from params import *

def build_printed_bolt():
    pitch = 5.0 * scale
    radius = 12.0 * scale
    
    # Bolt connects Handle -> Right Spool -> Left Spool
    # Full Threading!
    head_start = 162.0 * scale
    head_radius = 13.0 * scale
    head_thickness = 10.0 * scale
    head = Part.makeCylinder(head_radius, head_thickness, App.Vector(0,0,head_start))
    
    # Hex cut for turning
    hex_pts = []
    for i in range(7):
        angle = i * (math.pi / 3)
        hex_pts.append(App.Vector(6 * scale * math.cos(angle), 6 * scale * math.sin(angle), 0))
    hex_face = Part.Face(Part.Wire(Part.makePolygon(hex_pts)))
    hex_cut = hex_face.extrude(App.Vector(0, 0, 7 * scale))
    hex_cut.Placement = App.Placement(App.Vector(0,0,head_start + head_thickness - 6.9*scale), App.Rotation(0,0,0,1))
    
    # Slot cut
    slot = Part.makeBox(20*scale, 3.5*scale, 7*scale, App.Vector(-10*scale, -1.75*scale, head_start + head_thickness - 6.9*scale))
    head = head.cut(hex_cut).cut(slot)
    
    # 3. Threaded section (Fully threaded now)
    # Threads from Z = 15.0 to Z = 162.0 (Massive reduction from Z = -95 to Z = 162!)
    t_pitch = pitch
    desired_t_start = -100.0 * scale 
    t_start = round(desired_t_start / t_pitch) * t_pitch
    # Add overlap so the threads go inside the head and fuse properly
    t_length = (head_start - t_start) + 2.0 * scale
    t_r_inner = radius - (pitch * 0.45)
    
    helix = Part.makeHelix(pitch, t_length, t_r_inner, 0)
    
    inner_X = t_r_inner - 1.0 * scale
    p1 = App.Vector(inner_X, 0, -pitch*0.35)
    p2 = App.Vector(radius, 0, -pitch*0.1)
    p3 = App.Vector(radius, 0,  pitch*0.1)
    p4 = App.Vector(inner_X, 0,  pitch*0.35)
    wire = Part.Wire(Part.makePolygon([p1, p2, p3, p4, p1]))
    
    sweep = Part.Wire(helix).makePipeShell([wire], True, True)
    sweep.Placement = App.Placement(App.Vector(0,0,t_start), App.Rotation(0,0,0,1))
    
    # Extend core down to capture the floating down-curling sweep
    core_ext = pitch
    core = Part.makeCylinder(t_r_inner, t_length + core_ext, App.Vector(0,0,t_start - core_ext))
    
    # Avoid OpenCASCADE boolean hangs by using makeCompound for the final 3D printing export
    # The overlapping shapes (head, core, and thread sweep) slice perfectly in Bambu/PrusaSlicer
    bolt = Part.makeCompound([head, core, sweep])
    return bolt

if True:
    doc_name = "Doc_01_Center_Bolt"
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

    p_01_Bolt = build_printed_bolt()
    Part.show(p_01_Bolt, 'CenterBolt')
    print(f'Exporting 01_Center_Bolt...')
    p_01_Bolt.exportStl(os.path.join(export_dir, '01_Center_Bolt.stl'))
    p_01_Bolt.exportStep(os.path.join(export_dir, '01_Center_Bolt.step'))