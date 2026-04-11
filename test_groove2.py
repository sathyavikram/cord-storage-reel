import sys, os
sys.path.append('/Applications/FreeCAD.app/Contents/Resources/lib')
import FreeCAD as App
import Part
import math
scale = 1.0
axle_radius=30
half_axle=80
l_axle = Part.makeCylinder(axle_radius, half_axle, App.Vector(0,0,-half_axle))

cord_r = 4.5 * scale
g_pitch = 11.0 * scale
g_r_inner = axle_radius - cord_r
g_length = 160 + g_pitch * 4
g_start_z = -half_axle - g_pitch * 2

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

result = l_axle.cut(g_sweep)
print("Cut successful, volume:", result.Volume)
