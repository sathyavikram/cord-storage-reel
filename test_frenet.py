import sys, os
sys.path.append('/Applications/FreeCAD.app/Contents/Resources/lib')
import FreeCAD as App
import Part

g_pitch = 11.0; cord_r = 4.5; axle_radius = 30
g_r_inner = axle_radius - cord_r
g_helix = Part.makeHelix(g_pitch, 50, g_r_inner, 0)

# Local coordinates
# We want outer_X = 35, inner_X = 24.5 (g_r_inner - 1.0)
# Helix start is 25.5.
# With normal pointing INWARDS, outer_X must be negative!
# Local X = Helix_X - Desired_X
outer_X_loc = 25.5 - 35.0      # -9.5
inner_X_loc = 25.5 - 24.5 # -(-1.0)? Wait. inner_X was 24.5. So 25.5 - 24.5 = 1.0!

p1 = App.Vector(outer_X_loc, 0, -cord_r * 0.9)
p2 = App.Vector(inner_X_loc, 0, -cord_r * 0.4)
p3 = App.Vector(inner_X_loc, 0,  cord_r * 0.4)
p4 = App.Vector(outer_X_loc, 0,  cord_r * 0.9)
g_wire = Part.Wire(Part.makePolygon([p1, p2, p3, p4, p1]))

s3 = Part.Wire(g_helix).makePipeShell([g_wire], True, True)
print("s3 Bounding Box Max X =", s3.BoundBox.XMax)
