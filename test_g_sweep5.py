import sys, os
sys.path.append('/Applications/FreeCAD.app/Contents/Resources/lib')
import FreeCAD as App
import Part

g_pitch = 11.0; cord_r = 4.5; axle_radius = 30
g_length = 50.0

g_helix = Part.makeHelix(g_pitch, g_length, axle_radius, 0)

# Circle in XZ plane
g_circle = Part.Wire(Part.makeCircle(cord_r, App.Vector(axle_radius, 0, 0), App.Vector(0, 1, 0)))

g_sweep = Part.Wire(g_helix).makePipeShell([g_circle], True, True)

print("Bounding Box of Sweep with original circle strategy:", g_sweep.BoundBox)
