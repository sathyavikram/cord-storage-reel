import sys, os
_script_dir = os.getcwd()
sys.path.insert(0, _script_dir)
from part_01_spool_left import *

def build():
    clearance_amount = 0.4 * scale
    left_axle_pin_length = z_gap + hub_thickness + (5.0 * scale)
    l_pin_bearing = Part.makeCylinder(pin_radius, left_axle_pin_length, App.Vector(0,0, -half_axle - flange_thickness - left_axle_pin_length))
    
    anchor_tip_z = -half_axle - flange_thickness - left_axle_pin_length
    
    c_pitch = 5.0 * scale
    c_radius = 12.0 * scale + clearance_amount
    c_length = 65.0 * scale
    c_r_inner = 12.0 * scale - (c_pitch * 0.45) + clearance_amount
    
    c_helix = Part.makeHelix(c_pitch, c_length, c_r_inner, 0)
    
    inner_X = c_r_inner - 2.0 * scale
    p1 = App.Vector(inner_X, 0, -c_pitch*0.35)
    p2 = App.Vector(c_radius, 0, -c_pitch*0.1)
    p3 = App.Vector(c_radius, 0,  c_pitch*0.1)
    p4 = App.Vector(inner_X, 0,  c_pitch*0.35)
    c_wire = Part.Wire(Part.makePolygon([p1, p2, p3, p4, p1]))
    
    c_sweep = Part.Wire(c_helix).makePipeShell([c_wire], True, True)
    c_sweep.Placement = App.Placement(App.Vector(0,0,anchor_tip_z - 1.0), App.Rotation(0,0,0,1))
    c_core = Part.makeCylinder(c_r_inner, c_length, App.Vector(0,0,anchor_tip_z - 1.0))
    
    cap_cutter = c_core.fuse(c_sweep)
    
    chamfer = Part.makeCone(c_radius + 4, c_r_inner, c_pitch/2 + 4, App.Vector(0,0,anchor_tip_z - 2.0))
    cap_cutter = cap_cutter.fuse(chamfer)
    print("cap_cutter with chamfer:", cap_cutter.Volume, cap_cutter.isValid())

    l_pin_bearing_cut = l_pin_bearing.cut(cap_cutter)
    print("l_pin_bearing_cut volume:", l_pin_bearing_cut.Volume)

build()
