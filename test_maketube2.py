import sys, os
sys.path.append('/Applications/FreeCAD.app/Contents/Resources/lib')
import FreeCAD as App
import Part

scale = 1.0; cord_dia = 9.0 * scale; g_pitch = 11.0 * scale; cord_r = 4.5 * scale; axle_radius = 30 * scale
half_axle = 80 * scale
g_length = 160.0 + (g_pitch * 4)
g_start_z = -half_axle - (g_pitch * 2)

g_helix = Part.makeHelix(g_pitch, g_length, axle_radius, 0)
# Extract the edge from the helix
g_edge = g_helix.Edges[0]

g_tube = Part.makeTube(g_edge, cord_r)
g_tube.Placement = App.Placement(App.Vector(0,0,g_start_z), App.Rotation(0,0,0,1))

print("Tube bounding box:", g_tube.BoundBox)

l_axle = Part.makeCylinder(axle_radius, half_axle, App.Vector(0,0,-half_axle))
cut = l_axle.cut(g_tube)
print("Cut volume:", cut.Volume)
