import FreeCAD as App
import Part
from params import *

def build_caps():
    cap_thickness = 10 * scale
    cap_rad = pin_radius + 12 * scale

    cap_R = Part.makeCylinder(cap_rad, cap_thickness, App.Vector(0,0, half_axle + flange_thickness + pin_length - cap_thickness))
    c_R_sock = Part.makeCylinder(pin_radius + clearance, cap_thickness - 3*scale, App.Vector(0,0, half_axle + flange_thickness + pin_length - cap_thickness))
    cap_R = cap_R.cut(c_R_sock)

    cap_L = Part.makeCylinder(cap_rad, cap_thickness, App.Vector(0,0, -half_axle - flange_thickness - pin_length))
    c_L_sock = Part.makeCylinder(pin_radius + clearance, cap_thickness - 3*scale, App.Vector(0,0, -half_axle - flange_thickness - pin_length + 3*scale))
    cap_L = cap_L.cut(c_L_sock)

    return cap_R, cap_L
