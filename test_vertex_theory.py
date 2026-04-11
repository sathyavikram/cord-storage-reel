import sys, os
sys.path.append('/Applications/FreeCAD.app/Contents/Resources/lib')
import FreeCAD as App
import Part

# Curve is a line from (10,0,0) to (10,0,50)
curve = Part.makeLine((10,0,0), (10,0,50))

# Wire 1: points at X=20, 25
wire1 = Part.Wire(Part.makePolygon([App.Vector(20,0,0), App.Vector(25,0,0), App.Vector(25,0,1), App.Vector(20,0,1), App.Vector(20,0,0)]))

s1 = Part.Wire(curve).makePipeShell([wire1], True, True)

print("s1 bbox for line curve:", s1.BoundBox)

wire2 = Part.Wire(Part.makePolygon([App.Vector(-5,0,0), App.Vector(-10,0,0), App.Vector(-10,0,1), App.Vector(-5,0,1), App.Vector(-5,0,0)]))

s2 = Part.Wire(curve).makePipeShell([wire2], True, True)
print("s2 bbox for line curve:", s2.BoundBox)

