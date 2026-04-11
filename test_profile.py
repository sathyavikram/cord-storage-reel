import sys, os
sys.path.append('/Applications/FreeCAD.app/Contents/Resources/lib')
import FreeCAD as App
import Part
g_pitch = 11.0; cord_r = 4.5; axle_radius = 30
g_r_inner = axle_radius - cord_r
g_helix = Part.makeHelix(g_pitch, 50, g_r_inner, 0)

# Profile drawn at X=0
p1 = App.Vector(0, 0, -cord_r * 0.9)
p2 = App.Vector(axle_radius + 5 - g_r_inner, 0, -cord_r * 0.4)
p3 = App.Vector(axle_radius + 5 - g_r_inner, 0,  cord_r * 0.4)
p4 = App.Vector(0, 0,  cord_r * 0.9)
# wait, if drawn around X=0, it might sweep along the helix properly?
