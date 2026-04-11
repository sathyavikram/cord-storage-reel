import sys, os
sys.path.append('/Applications/FreeCAD.app/Contents/Resources/lib')
import FreeCAD as App
import Part
import math
scale = 1.0
axle_radius=30
axle_length=160
half_axle=80
l_axle = Part.makeCylinder(axle_radius, half_axle, App.Vector(0,0,-half_axle))
cord_dia = 9.0 * scale
g_pitch = cord_dia + (2.0 * scale)
g_r = cord_dia / 2.0
g_start_z = -half_axle - g_pitch
g_length = axle_length + 2 * g_pitch
g_helix = Part.makeHelix(g_pitch, g_length, axle_radius, 0)
g_circle = Part.Wire(Part.makeCircle(g_r, App.Vector(axle_radius, 0, 0), App.Vector(0, 1, g_pitch / (2 * math.pi * axle_radius))))
g_sweep = Part.Wire(g_helix).makePipeShell([g_circle], True, True)
g_sweep.Placement = App.Placement(App.Vector(0,0,g_start_z), App.Rotation(0,0,0,1))
result = l_axle.cut(g_sweep)
print("Cut successful, volume:", result.Volume)
