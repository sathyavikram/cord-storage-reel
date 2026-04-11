import sys, os
sys.path.append('/Applications/FreeCAD.app/Contents/Resources/lib')
import Part

g_pitch = 11.0; cord_r = 4.5; axle_radius = 30; g_length = 50.0

g_helix = Part.makeHelix(g_pitch, g_length, axle_radius, 0)
g_tube = Part.makeTube(g_helix, cord_r)

print("BoundBox of Tube:", g_tube.BoundBox)
g_tube.exportStep("tube.step")
