import sys, os
_script_dir = os.getcwd()
sys.path.insert(0, _script_dir)
from part_01_spool_left import *

def test():
    l_flange = Part.makeCylinder(flange_radius, flange_thickness, App.Vector(0,0, -half_axle - flange_thickness))
    l_axle = Part.makeCylinder(axle_radius, half_axle, App.Vector(0,0,-half_axle))
    left_axle_pin_length = z_gap + hub_thickness + (5.0 * scale)
    l_pin_bearing = Part.makeCylinder(pin_radius, left_axle_pin_length, App.Vector(0,0, -half_axle - flange_thickness - left_axle_pin_length))

    left_spool = l_flange.fuse(l_axle).fuse(l_pin_bearing)
    print("V_base:", left_spool.Volume)

    rib_thickness = 4.0 * scale
    rib_height = 20.0 * scale
    rib_length = 35.0 * scale
    rib_wire = Part.Wire(Part.makePolygon([
        App.Vector(axle_radius - 1, 0, -half_axle),
        App.Vector(axle_radius - 1, 0, -half_axle + rib_height),
        App.Vector(axle_radius - 1 + rib_length, 0, -half_axle),
        App.Vector(axle_radius - 1, 0, -half_axle)
    ]))
    rib_face = Part.Face(rib_wire)
    rib_solid = rib_face.extrude(App.Vector(0, rib_thickness, 0))
    rib_solid.translate(App.Vector(0, -rib_thickness/2.0, 0))

    rib0 = rib_solid.copy()
    left_spool = left_spool.fuse(rib0)
    print("V_rib0:", left_spool.Volume, left_spool.isValid())

test()
