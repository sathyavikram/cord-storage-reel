import sys, os
sys.path.append('/Applications/FreeCAD.app/Contents/Resources/lib')
import FreeCAD as App
import Part

scale = 1.0; g_pitch = 11.0; cord_r = 4.5; axle_radius = 30
half_axle = 80; g_length = 160.0

g_helix = Part.makeHelix(g_pitch, g_length, axle_radius, 0)
# Normal points INWARD (-X in global initially)
# Binormal points generally UP (+Z in global)
# Tangent points ALONG the helix curve (+Y in global)

# The profile for pipe shell is expected in the Normal-Binormal plane! (i.e. XY in wire coords)
# 'X' of wire = Normal (Inward)
# 'Y' of wire = Binormal (Up along the axle)

# Draw profile in wire coords:
# We want depth cord_r inward: X from -2.0 (outside axle) to cord_r (inside axle) 
# We want width cord_r*2, so Y from -cord_r to +cord_r

X_out = -2.0
X_in = cord_r
Y_bottom = -cord_r * 0.9
Y_top = cord_r * 0.9
Y_in_bottom = -cord_r * 0.4
Y_in_top = cord_r * 0.4

p1 = App.Vector(X_out, Y_bottom, 0)
p2 = App.Vector(X_in,  Y_in_bottom, 0)
p3 = App.Vector(X_in,  Y_in_top, 0)
p4 = App.Vector(X_out, Y_top, 0)
wire = Part.Wire(Part.makePolygon([p1, p2, p3, p4, p1]))

sweep = Part.Wire(g_helix).makePipeShell([wire], True, True)  # solid, frenet
print("Sweep BoundBox with proper local XY profile:", sweep.BoundBox)

l_axle = Part.makeCylinder(axle_radius, half_axle, App.Vector(0,0,-half_axle))
sweep.Placement = App.Placement(App.Vector(0,0,-half_axle), App.Rotation(0,0,0,1))
cut = l_axle.cut(sweep)
print("Cut volume:", cut.Volume)
cut.exportStep('final_good_cut.step')
