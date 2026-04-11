import sys, os
sys.path.append('/Applications/FreeCAD.app/Contents/Resources/lib')
import FreeCAD as App
import Part
t_pitch = 11.0; t_radius = 30.0; t_r_inner = 25.5
t_helix = Part.makeHelix(t_pitch, 30, t_r_inner, 0)
p1 = App.Vector(t_r_inner - 1, 0, -2)
p2 = App.Vector(t_radius + 5, 0, -1)
p3 = App.Vector(t_radius + 5, 0,  1)
p4 = App.Vector(t_r_inner - 1, 0,  2)
wire = Part.Wire(Part.makePolygon([p1, p2, p3, p4, p1]))
s1 = Part.Wire(t_helix).makePipeShell([wire], True, True)

print("BoundingBox max X is:", s1.BoundBox.XMax)
