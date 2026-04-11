import sys, os
sys.path.append('/Applications/FreeCAD.app/Contents/Resources/lib')
import FreeCAD as App
import Part
scale = 1.0
cord_dia = 9.0 * scale
g_pitch = 11.0 * scale
cord_r = 4.5 * scale
axle_length=160
axle_radius=30
half_axle = axle_length/2.0

g_length = axle_length + (g_pitch * 4)
g_start_z = -half_axle - (g_pitch * 2)
g_r_inner = axle_radius - cord_r
g_helix = Part.makeHelix(g_pitch, g_length, g_r_inner, 0)
inner_X = g_r_inner - 1.0 * scale
outer_X = axle_radius + 5.0 * scale

p1 = App.Vector(outer_X, 0, -cord_r * 0.9)
p2 = App.Vector(inner_X, 0, -cord_r * 0.4)
p3 = App.Vector(inner_X, 0,  cord_r * 0.4)
p4 = App.Vector(outer_X, 0,  cord_r * 0.9)
g_wire = Part.Wire(Part.makePolygon([p1, p2, p3, p4, p1]))
g_sweep = Part.Wire(g_helix).makePipeShell([g_wire], True, True)
g_sweep.Placement = App.Placement(App.Vector(0,0,g_start_z), App.Rotation(0,0,0,1))

print("g_sweep volume:", g_sweep.Volume)
print("g_sweep bbox:", g_sweep.BoundBox)

l_axle = Part.makeCylinder(axle_radius, half_axle, App.Vector(0,0,-half_axle))
cut = l_axle.cut(g_sweep)
print("l_axle cut volume:", cut.Volume)
