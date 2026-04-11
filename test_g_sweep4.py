import sys, os
sys.path.append('/Applications/FreeCAD.app/Contents/Resources/lib')
import FreeCAD as App
import Part

g_pitch = 11.0; cord_r = 4.5; axle_radius = 30
g_r_inner = axle_radius - cord_r
g_helix = Part.makeHelix(g_pitch, 100, g_r_inner, 0)

# Wire drawn AROUND X=0
inner_X_rel = 0
outer_X_rel = 5.0 + cord_r  # 5 + 4.5 = 9.5
p1 = App.Vector(outer_X_rel, 0, -cord_r * 0.9)
p2 = App.Vector(inner_X_rel, 0, -cord_r * 0.4)
p3 = App.Vector(inner_X_rel, 0,  cord_r * 0.4)
p4 = App.Vector(outer_X_rel, 0,  cord_r * 0.9)
g_wire = Part.Wire(Part.makePolygon([p1, p2, p3, p4, p1]))
s1 = Part.Wire(g_helix).makePipeShell([g_wire], True, True)

print("Bounding box when wire is around X=0:", s1.BoundBox)
s1.exportStep("thread_x0.step")
