import sys, os
sys.path.append('/Applications/FreeCAD.app/Contents/Resources/lib')
import FreeCAD as App
import Part

g_pitch = 11.0; cord_r = 4.5; axle_radius = 30
g_r_inner = axle_radius - cord_r
g_helix = Part.makeHelix(g_pitch, 50, g_r_inner, 0)

# the start of the helix is at (g_r_inner, 0, 0).
# Let's draw the wire such that the inner edge is at X = g_r_inner
inner_X = g_r_inner
outer_X = axle_radius + 5.0
p1 = App.Vector(outer_X, 0, -cord_r * 0.9)
p2 = App.Vector(inner_X, 0, -cord_r * 0.4)
p3 = App.Vector(inner_X, 0,  cord_r * 0.4)
p4 = App.Vector(outer_X, 0,  cord_r * 0.9)
g_wire = Part.Wire(Part.makePolygon([p1, p2, p3, p4, p1]))

s1 = Part.Wire(g_helix).makePipeShell([g_wire], True, True)
print("Bounding Box Max X =", s1.BoundBox.XMax)

# Now evaluate where the closest point mapping happens!
