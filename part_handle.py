import FreeCAD as App
import Part
from params import *

def build_handle():
    h_z = half_axle + flange_thickness 
    h_peg = Part.makeCylinder(handle_peg_radius, flange_thickness, App.Vector(hole_dist, 0, h_z - flange_thickness))
    h_shield = Part.makeCylinder(22*scale, 8*scale, App.Vector(hole_dist, 0, h_z)) 
    h_grip = Part.makeCylinder(14*scale, 65*scale, App.Vector(hole_dist, 0, h_z + 8*scale))
    return h_peg.fuse(h_shield).fuse(h_grip).removeSplitter()
