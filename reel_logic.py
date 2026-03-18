import FreeCAD as App
import Part
import math
import os

doc = App.newDocument()

# Design Parameters for Heavy Duty Extension Cord (150 ft 14/3 Gauge)
flange_radius = 120         # 240mm diameter to hold 150ft cord securely
flange_thickness = 15       # Solid thickness
axle_radius = 30            # 60mm diameter axle, safer bend radius for 14/3 cord
axle_length = 190           # Maximized length (190) fitting inside 256mm build plate footprint
handle_length = 100
handle_arm_thickness = 10
handle_grip_radius = 12
handle_grip_length = 80

pin_radius = 15             # 30mm diameter pins holding the reel structure
hub_hole_radius = 20        # Creates EXACTLY a 5mm radial gap between the axle pin and the ring
hub_radius = 50             # 100mm diameter stand connecting rings matching the axle
hub_thickness = 26          # 10mm thicker than the 16mm stand diameter, completely enveloping it

# Total 5mm z-axis longitudinal gap between reel and stand
z_gap = 5 

# --- Reel Body ---
# Flange 1 (Left)
f1 = Part.makeCylinder(flange_radius, flange_thickness, App.Vector(0,0,0))
# Flange 2 (Right)
f2 = Part.makeCylinder(flange_radius, flange_thickness, App.Vector(0, 0, axle_length - flange_thickness))

flanges_with_holes = f1.fuse(f2)
hole_radius = 30
hole_dist = 70
for i in range(6):
    angle = math.radians(i * 60)
    hx = hole_dist * math.cos(angle)
    hy = hole_dist * math.sin(angle)
    cutter = Part.makeCylinder(hole_radius, axle_length + 20, App.Vector(hx, hy, -10))
    flanges_with_holes = flanges_with_holes.cut(cutter)

axle = Part.makeCylinder(axle_radius, axle_length)

# Left Pin & Cap
# Pin pulls back by (z_gap + hub_thickness + 5mm external gap) = 5 + 26 + 5 = 36mm. Z starts at -36.
left_pin = Part.makeCylinder(pin_radius, 36, App.Vector(0,0,-36))
# Cap acts as external lock on the stand hub, leaving a 5mm gap
left_cap = Part.makeCylinder(25, 5, App.Vector(0,0,-41))

# Right Pin & Handle Base
# Pin reaches forward by (z_gap + hub_thickness + 5) = 36mm out of axle
right_pin = Part.makeCylinder(pin_radius, 36, App.Vector(0, 0, axle_length))

# Handle Arm sits exactly at Z = axle_length + 36 (guaranteeing 5mm gap after the hub ends)
handle_z = axle_length + 36 
arm_box = Part.makeBox(handle_length, 24, handle_arm_thickness, App.Vector(0, -12, handle_z))
arm_base = Part.makeCylinder(16, handle_arm_thickness, App.Vector(0, 0, handle_z))
arm_end = Part.makeCylinder(16, handle_arm_thickness, App.Vector(handle_length, 0, handle_z))
arm = arm_box.fuse(arm_base).fuse(arm_end)

# Handle Grip extending from front arm towards viewer
grip = Part.makeCylinder(handle_grip_radius, handle_grip_length, App.Vector(handle_length, 0, handle_z + handle_arm_thickness))

# Combine reel parts
reel = flanges_with_holes.fuse(axle).fuse(left_pin).fuse(left_cap).fuse(right_pin).fuse(arm).fuse(grip)
reel = reel.removeSplitter()

# --- Stand ---
z_left = -18   # Center of left hub
z_right = axle_length + 18  # Center of right hub dynamically spaced

y_floor = -140
x_spread = 90
y_handle = 150
pipe_radius = 8

def make_pipe(p1, p2, r):
    direction = p2 - p1
    return Part.makeCylinder(r, direction.Length, p1, direction)

p_hub_L = App.Vector(0, 0, z_left)
p_fl_L = App.Vector(x_spread, y_floor, z_left)
p_bl_L = App.Vector(-x_spread, y_floor, z_left)

p_hub_R = App.Vector(0, 0, z_right)
p_fr_R = App.Vector(x_spread, y_floor, z_right)
p_br_R = App.Vector(-x_spread, y_floor, z_right)

p_top_L = App.Vector(0, y_handle, z_left)
p_top_R = App.Vector(0, y_handle, z_right)

pipes = [
    make_pipe(p_hub_L, p_fl_L, pipe_radius),
    make_pipe(p_hub_L, p_bl_L, pipe_radius),
    make_pipe(p_hub_R, p_fr_R, pipe_radius),
    make_pipe(p_hub_R, p_br_R, pipe_radius),
    make_pipe(p_fl_L, p_fr_R, pipe_radius),
    make_pipe(p_bl_L, p_br_R, pipe_radius),
    make_pipe(p_hub_L, p_top_L, pipe_radius),
    make_pipe(p_hub_R, p_top_R, pipe_radius),
    make_pipe(p_top_L, p_top_R, pipe_radius)
]

# Add spheres at the pipe intersections to create perfectly smooth rounded corners (fillets)
joint_points = [p_hub_L, p_fl_L, p_bl_L, p_hub_R, p_fr_R, p_br_R, p_top_L, p_top_R]
joints = [Part.makeSphere(pipe_radius, pt) for pt in joint_points]

stand = pipes[0]
for p in pipes[1:]:
    stand = stand.fuse(p)
for j in joints:
    stand = stand.fuse(j)

# Stand Hubs mapping exact spacing. 
# Z-axis for left pin cap drops up to -41. Z axis starts at -36 for pin.
# Flange is at 0. So left gap is from -31 to -5. The hub should exactly occupy -31 to -5 (thickness 26mm).
# On the right, axle ends at 190. Then 5mm gap. Right Pin extends from 190 to 226. Right hub ends at 195+26 = 221. Handle starts at 226.
hub_L = Part.makeCylinder(hub_radius, hub_thickness, App.Vector(0, 0, -31))
hub_R = Part.makeCylinder(hub_radius, hub_thickness, App.Vector(0, 0, axle_length + 5))

# Fuse the solid rings to the stand FIRST so the pipes blend into the rings
stand = stand.fuse(hub_L).fuse(hub_R)

# NOW cut the holes completely out of the resulting stand.
# This removes any pipe segments that intersected into the center hole, ensuring 0% friction!
hub_L_hole = Part.makeCylinder(hub_hole_radius, hub_thickness + 20, App.Vector(0, 0, -41))
hub_R_hole = Part.makeCylinder(hub_hole_radius, hub_thickness + 20, App.Vector(0, 0, axle_length))

stand = stand.cut(hub_L_hole).cut(hub_R_hole)
stand = stand.removeSplitter()

# Final assembly creation logic generating individual and compound solids internally
final_shape = Part.makeCompound([reel, stand])

obj = doc.addObject("Part::Feature", "Reel_with_Handle")
obj.Shape = final_shape

export_dir = "/Users/intelligentmachine/Documents/workspace/3d-models/cord-storage-reel-v3/exports"
if not os.path.exists(export_dir):
    os.makedirs(export_dir)

final_shape.exportStep(os.path.join(export_dir, "flange-axle-handle.step"))
final_shape.exportStl(os.path.join(export_dir, "flange-axle-handle.stl"))

Part.show(final_shape)

