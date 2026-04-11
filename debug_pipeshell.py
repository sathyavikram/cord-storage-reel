import sys, os
sys.path.append('/Applications/FreeCAD.app/Contents/Resources/lib')
import FreeCAD as App
import Part

g_r_inner = 25.5
g_helix = Part.makeHelix(11.0, 160.0, g_r_inner, 0)

print("Test 1: Wire at X = 0")
p1 = App.Vector(0, 0, -4.0); p2 = App.Vector(10, 0, -2.0)
p3 = App.Vector(10, 0,  2.0); p4 = App.Vector(0, 0,  4.0)
w1 = Part.Wire(Part.makePolygon([p1, p2, p3, p4, p1]))
s1 = Part.Wire(g_helix).makePipeShell([w1], True, True)
print("s1 BBox:", s1.BoundBox)

print("Test 2: Wire at X = 25.5")
p1 = App.Vector(25.5, 0, -4.0); p2 = App.Vector(35.5, 0, -2.0)
p3 = App.Vector(35.5, 0,  2.0); p4 = App.Vector(25.5, 0,  4.0)
w2 = Part.Wire(Part.makePolygon([p1, p2, p3, p4, p1]))
s2 = Part.Wire(g_helix).makePipeShell([w2], True, True)
print("s2 BBox:", s2.BoundBox)
