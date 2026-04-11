import sys, os
import math
sys.path.append('/Applications/FreeCAD.app/Contents/Resources/lib')
import FreeCAD as App
import Part

g_pitch = 11.0; cord_r = 4.5; axle_radius = 30
g_length = 50.0

g_helix = Part.makeHelix(g_pitch, g_length, axle_radius, 0)

# Tilted Circle in XZ plane
g_circle = Part.Wire(Part.makeCircle(cord_r, App.Vector(axle_radius, 0, 0), App.Vector(0, 1, g_pitch / (2 * math.pi * axle_radius))))

g_sweep = Part.Wire(g_helix).makePipeShell([g_circle], True, True)

print("Bounding Box of Tilted Circle Sweep:", g_sweep.BoundBox)
