import sys, os
sys.path.append('/Applications/FreeCAD.app/Contents/Resources/lib')
import FreeCAD as App
import Part

print("Building swept thread using actual FreeCAD sweep method...")
t_pitch = 11.0; t_radius = 30.0; t_r_inner = 25.5
t_helix = Part.makeHelix(t_pitch, 50, t_r_inner, 0)

# Wire drawn at X=t_inner_r
p1 = App.Vector(t_r_inner - 1, 0, -2)
p2 = App.Vector(t_radius + 5, 0, -1)
p3 = App.Vector(t_radius + 5, 0,  1)
p4 = App.Vector(t_r_inner - 1, 0,  2)
wire = Part.Wire(Part.makePolygon([p1, p2, p3, p4, p1]))

# In FreeCAD, the standard way to do threads is sweep().
face = Part.Face(wire)
sweep = face.sweep(Part.Wire(t_helix), 1, 0, 1) # solid=1, frenet=1
print("sweep bbox:", sweep.BoundBox)
sweep.exportStep('test_frenet_sweep.step')
