import sys, os
sys.path.append('/Applications/FreeCAD.app/Contents/Resources/lib')
import FreeCAD as App
import Part

scale = 1.0; cord_dia = 9.0 * scale; g_pitch = 11.0 * scale; cord_r = 4.5 * scale; axle_radius = 30 * scale
half_axle = 80 * scale
g_length = 160.0 + (g_pitch * 4)
g_start_z = -half_axle - (g_pitch * 2)

g_helix = Part.makeHelix(g_pitch, g_length, axle_radius, 0)

# Wire drawn at the origin
p1 = App.Vector(5.0, 0, -cord_r * 0.9)
p2 = App.Vector(-cord_r, 0, -cord_r * 0.4)
p3 = App.Vector(-cord_r, 0,  cord_r * 0.4)
p4 = App.Vector(5.0, 0,  cord_r * 0.9)
g_wire = Part.Wire(Part.makePolygon([p1, p2, p3, p4, p1]))

g_sweep = Part.Wire(g_helix).makePipeShell([g_wire], True, True)
g_sweep.Placement = App.Placement(App.Vector(0,0,g_start_z), App.Rotation(0,0,0,1))

print("Sweep bounding box:", g_sweep.BoundBox)

l_axle = Part.makeCylinder(axle_radius, half_axle, App.Vector(0,0,-half_axle))
cut = l_axle.cut(g_sweep)
print("Cut volume:", cut.Volume)
