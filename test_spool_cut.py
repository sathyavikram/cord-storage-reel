import sys, os
_script_dir = os.getcwd()
sys.path.insert(0, _script_dir)
from part_01_spool_left import *

def build_left_spool_debug():
    l_flange = Part.makeCylinder(flange_radius, flange_thickness, App.Vector(0,0, -half_axle - flange_thickness))
    l_axle = Part.makeCylinder(axle_radius, half_axle, App.Vector(0,0,-half_axle))

    cord_dia = 9.0 * scale
    g_pitch = 11.0 * scale
    cord_r = 4.5 * scale
    g_length = axle_length + (g_pitch * 4)
    g_start_z = -half_axle - (g_pitch * 2)
    g_r_inner = axle_radius - cord_r
    
    g_helix = Part.makeHelix(g_pitch, g_length, g_r_inner, 0)
    inner_X = g_r_inner - 1.0 * scale
    outer_X = axle_radius + 5.0 * scale
    
    p1 = App.Vector(outer_X, 0, -cord_r * 0.9)
    p2 = App.Vector(inner_X, 0, -cord_r * 0.4)
    p3 = App.Vector(inner_X, 0,  cord_r * 0.4)
    p4 = App.Vector(outer_X, 0,  cord_r * 0.9)
    g_wire = Part.Wire(Part.makePolygon([p1, p2, p3, p4, p1]))
    g_sweep = Part.Wire(g_helix).makePipeShell([g_wire], True, True)
    g_sweep.Placement = App.Placement(App.Vector(0,0,g_start_z), App.Rotation(0,0,0,1))
    l_axle = l_axle.cut(g_sweep)

    def make_hex_prism(radius, length, placement):
        pts = []
        for i in range(7):
            angle = i * (math.pi / 3)
            pts.append(App.Vector(radius * math.cos(angle), radius * math.sin(angle), 0))
        face = Part.Face(Part.Wire(Part.makePolygon(pts)))
        prism = face.extrude(App.Vector(0, 0, length))
        prism.Placement = placement
        return prism

    clearance_amount = 0.4 * scale
    hex_depth = 50.0 * scale
    l_axle_hole = make_hex_prism(peg_radius + clearance_amount, hex_depth, App.Placement(App.Vector(0,0,-hex_depth + 1.0 * scale), App.Rotation(0,0,0,1)))

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

    for i in range(6):
        angle = math.radians(i * 60)
        hx = hole_dist * math.cos(angle)
        hy = hole_dist * math.sin(angle)
        cutter = Part.makeCylinder(hole_radius, flange_thickness + 10, App.Vector(hx, hy, -half_axle - flange_thickness - 5))
        l_flange = l_flange.cut(cutter)
    
    rib_thickness = 4.0 * scale
    rib_height = 20.0 * scale
    rib_length = 35.0 * scale
    
    rib_wire = Part.Wire(Part.makePolygon([
        App.Vector(axle_radius - 1, 0, -half_axle),
        App.Vector(axle_radius - 1 + rib_length, 0, -half_axle),
        App.Vector(axle_radius - 1, 0, -half_axle + rib_height),
        App.Vector(axle_radius - 1, 0, -half_axle)
    ]))
    rib_face = Part.Face(rib_wire)
    rib_solid = rib_face.extrude(App.Vector(0, rib_thickness, 0))
    rib_solid.translate(App.Vector(0, -rib_thickness/2.0, 0))
    
    ribs = []
    for i in range(6):
        angle = math.radians(i * 60 + 30)
        rib = rib_solid.copy()
        rib.rotate(App.Vector(0,0,0), App.Vector(0,0,1), math.degrees(angle))
        ribs.append(rib)
    
    left_spool = l_flange.fuse(l_axle).fuse(l_pin_bearing)
    print("V1:", left_spool.Volume)
    for r in ribs:
        left_spool = left_spool.fuse(r)
    print("V2:", left_spool.Volume)
    
    left_spool = left_spool.cut(l_axle_hole)
    print("V3:", left_spool.Volume)
    
    # Actually cut the cap threaded hole from the spool
    left_spool = left_spool.cut(cap_cutter)
    print("V4:", left_spool.Volume)
    left_spool = left_spool.removeSplitter()
    print("V5:", left_spool.Volume)

build_left_spool_debug()
