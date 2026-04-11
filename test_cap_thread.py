import sys, os
sys.path.append('/Applications/FreeCAD.app/Contents/Resources/lib')
import FreeCAD as App
import Part
t_pitch = 5.0
extra_clearance = 0.4
t_radius = 12.0 - extra_clearance
t_length = 60.0
t_r_inner = t_radius - (t_pitch * 0.45)
t_helix = Part.makeHelix(t_pitch, t_length, t_r_inner, 0)
inner_X = t_r_inner - 2.0
p1 = App.Vector(inner_X, 0, -t_pitch*0.35)
p2 = App.Vector(t_radius, 0, -t_pitch*0.1)
p3 = App.Vector(t_radius, 0,  t_pitch*0.1)
p4 = App.Vector(inner_X, 0,  t_pitch*0.35)
t_wire = Part.Wire(Part.makePolygon([p1, p2, p3, p4, p1]))
t_sweep = Part.Wire(t_helix).makePipeShell([t_wire], True, True)
print("cap thread bounding box:", t_sweep.BoundBox)
print("cap thread volume:", t_sweep.Volume)
