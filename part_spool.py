import FreeCAD as App
import Part
import math
from params import *

def build_right_spool():
    r_flange = Part.makeCylinder(flange_radius, flange_thickness, App.Vector(0,0, half_axle))
    r_axle = Part.makeCylinder(axle_radius, half_axle, App.Vector(0,0,0))
    
    r_axle_peg = Part.makeCylinder(peg_radius, 25*scale, App.Vector(0,0,-25*scale))
    r_pin = Part.makeCylinder(pin_radius, pin_length, App.Vector(0,0, half_axle + flange_thickness))

    for i in range(6):
        angle = math.radians(i * 60)
        hx = hole_dist * math.cos(angle)
        hy = hole_dist * math.sin(angle)
        cutter = Part.makeCylinder(hole_radius, flange_thickness + 10, App.Vector(hx, hy, half_axle - 5))
        r_flange = r_flange.cut(cutter)

    handle_hole = Part.makeCylinder(handle_peg_radius + clearance, flange_thickness + 10, App.Vector(hole_dist, 0, half_axle - 5))
    r_flange = r_flange.cut(handle_hole)

    right_spool = r_flange.fuse(r_axle).fuse(r_axle_peg).fuse(r_pin)
    return right_spool.removeSplitter()

def build_left_spool():
    l_flange = Part.makeCylinder(flange_radius, flange_thickness, App.Vector(0,0, -half_axle - flange_thickness))
    l_axle = Part.makeCylinder(axle_radius, half_axle, App.Vector(0,0,-half_axle))
    
    l_axle_hole = Part.makeCylinder(peg_radius + clearance, 30*scale, App.Vector(0,0,-28*scale)) 
    l_pin = Part.makeCylinder(pin_radius, pin_length, App.Vector(0,0, -half_axle - flange_thickness - pin_length))

    for i in range(6):
        angle = math.radians(i * 60)
        hx = hole_dist * math.cos(angle)
        hy = hole_dist * math.sin(angle)
        cutter = Part.makeCylinder(hole_radius, flange_thickness + 10, App.Vector(hx, hy, -half_axle - flange_thickness - 5))
        l_flange = l_flange.cut(cutter)
        
    left_spool = l_flange.fuse(l_axle).fuse(l_pin).cut(l_axle_hole)
    return left_spool.removeSplitter()
