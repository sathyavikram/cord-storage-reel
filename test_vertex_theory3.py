import sys, os
sys.path.append('/Applications/FreeCAD.app/Contents/Resources/lib')
import FreeCAD as App
import Part

helix = Part.makeHelix(11, 50, 10, 0)
# Helix begins at X=10, Y=0, Z=0

# Wire centered around X=-15 
wire2 = Part.Wire(Part.makePolygon([App.Vector(-15,0,0), App.Vector(-10,0,0), App.Vector(-10,0,1), App.Vector(-15,0,1), App.Vector(-15,0,0)]))
s2 = Part.Wire(helix).makePipeShell([wire2], True, True)

print("s2 bbox for helix (-15):", s2.BoundBox)
