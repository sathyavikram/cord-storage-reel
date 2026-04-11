import sys, os
sys.path.append('/Applications/FreeCAD.app/Contents/Resources/lib')
import FreeCAD as App
import Part

helix = Part.makeHelix(11, 50, 10, 0)
wire1 = Part.Wire(Part.makePolygon([App.Vector(20,0,0), App.Vector(25,0,0), App.Vector(25,0,1), App.Vector(20,0,1), App.Vector(20,0,0)]))
s1 = Part.Wire(helix).makePipeShell([wire1], True, True)

print("s1 bbox for helix:", s1.BoundBox)
