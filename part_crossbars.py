import FreeCAD as App
import Part
from params import *

def build_crossbars():
    bar_len = (z_R + hub_thickness/2) - (z_L - hub_thickness/2)
    z_origin = z_L - hub_thickness/2

    bar1 = Part.makeCylinder(crossbar_radius, bar_len, App.Vector(x_spread, y_floor, z_origin))
    bar2 = Part.makeCylinder(crossbar_radius, bar_len, App.Vector(-x_spread, y_floor, z_origin))
    bar3 = Part.makeCylinder(crossbar_radius, bar_len, App.Vector(0, y_top, z_origin))
    
    return bar1, bar2, bar3
