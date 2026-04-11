import sys, os
sys.path.append('/Applications/FreeCAD.app/Contents/Resources/lib')
import FreeCAD as App
import Part

g_pitch = 11.0; cord_r = 4.5; axle_radius = 30
g_r_inner = axle_radius - cord_r
g_helix = Part.makeHelix(g_pitch, 100, g_r_inner, 0)

inner_X = g_r_inner - 1.0; outer_X = axle_radius + 5.0
p1 = App.Vector(outer_X - g_r_inner, 0, -cord_r * 0.9)
p2 = App.Vector(inner_X - g_r_inner, 0, -cord_r * 0.4)
p3 = App.Vector(inner_X - g_r_inner, 0,  cord_r * 0.4)
p4 = App.Vector(outer_X - g_r_inner, 0,  cord_r * 0.9)

g_wire2 = Part.Wire(Part.makePolygon([p1, p2, p3, p4, p1]))
s2 = Part.Wire(g_helix).makePipeShell([g_wire2], True, True)

print("s2 bound box (relative coords):", s2.BoundBox)
s2.exportStep('s2_helix.step')

# What if helix has radius 0, so it's a straight line up Z, but wait, helix CANNOT have radius 0.
