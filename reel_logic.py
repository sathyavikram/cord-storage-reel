import FreeCAD as App
import Part
import math
import os

doc = App.newDocument()

# Design Parameters for Heavy Duty Extension Cord
# By default, user_scale = 1.0 is engineered to precisely fit a massive 350x350x350mm build envelope.
# This yields a total maximum storage capacity of approx ~150 FT of thick 14/3 Gauge Extension Cord!
# For a 300x300x300mm plate (e.g. Prusa XL), change this to 0.85
# For a 256x256x256mm plate (e.g. Bambu Lab), change this to 0.73
# For a 180x180x180mm plate (e.g. Prusa Mini), change this to 0.50
user_scale = 0.5

# Internal math adapter: To make user_scale = 1.0 hit exactly ~345mm wide/tall bounds.
scale = user_scale * 0.95

flange_radius = 120 * scale         # scaled diameter to hold cord
flange_thickness = 15 * scale       # Solid thickness
axle_radius = 30 * scale            # scaled axle radius
axle_length = 200 * scale           # Maximized length fitting inside footprint
handle_length = 100 * scale
handle_arm_thickness = 10 * scale
handle_grip_radius = 12 * scale
handle_grip_length = 80 * scale

pin_radius = 15 * scale             # pins holding the reel structure
hub_hole_radius = 20 * scale        # radial gap between the axle pin and the ring
hub_radius = 50 * scale             # stand connecting rings matching the axle
hub_thickness = 26 * scale          # thicker than the stand diameter

# Total longitudinal gap between reel and stand
z_gap = 5 * scale 

# --- Reel Body ---
# Flange 1 (Left)
f1 = Part.makeCylinder(flange_radius, flange_thickness, App.Vector(0,0,0))
# Flange 2 (Right)
f2 = Part.makeCylinder(flange_radius, flange_thickness, App.Vector(0, 0, axle_length - flange_thickness))

flanges_with_holes = f1.fuse(f2)
hole_radius = 30 * scale
hole_dist = 70 * scale
for i in range(6):
    angle = math.radians(i * 60)
    hx = hole_dist * math.cos(angle)
    hy = hole_dist * math.sin(angle)
    cutter = Part.makeCylinder(hole_radius, axle_length + 20*scale, App.Vector(hx, hy, -10*scale))
    flanges_with_holes = flanges_with_holes.cut(cutter)

axle = Part.makeCylinder(axle_radius, axle_length)

# Left Pin & Cap
pin_left_ext = z_gap + hub_thickness + (5*scale)
left_pin = Part.makeCylinder(pin_radius, pin_left_ext, App.Vector(0,0,-pin_left_ext))
left_cap = Part.makeCylinder(25*scale, 5*scale, App.Vector(0,0,-(pin_left_ext + 5*scale)))

# Right Pin & Handle Base
right_pin_ext = z_gap + hub_thickness + (5*scale)
right_pin = Part.makeCylinder(pin_radius, right_pin_ext, App.Vector(0, 0, axle_length))

# Handle Arm sits exactly at Z = axle_length + right_pin_ext
handle_z = axle_length + right_pin_ext 
arm_box = Part.makeBox(handle_length, 24*scale, handle_arm_thickness, App.Vector(0, -12*scale, handle_z))
arm_base = Part.makeCylinder(16*scale, handle_arm_thickness, App.Vector(0, 0, handle_z))
arm_end = Part.makeCylinder(16*scale, handle_arm_thickness, App.Vector(handle_length, 0, handle_z))
arm = arm_box.fuse(arm_base).fuse(arm_end)

# Handle Grip extending from front arm towards viewer
grip = Part.makeCylinder(handle_grip_radius, handle_grip_length, App.Vector(handle_length, 0, handle_z + handle_arm_thickness))

# Combine reel parts
reel = flanges_with_holes.fuse(axle).fuse(left_pin).fuse(left_cap).fuse(right_pin).fuse(arm).fuse(grip)
reel = reel.removeSplitter()

# --- Stand ---
z_left = -18 * scale   # Center of left hub
z_right = axle_length + (18 * scale)  # Center of right hub dynamically spaced

y_floor = -140 * scale
x_spread = 90 * scale
y_handle = 150 * scale
pipe_radius = 8 * scale

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

# Stand Hubs mapping exact spacing
hub_L = Part.makeCylinder(hub_radius, hub_thickness, App.Vector(0, 0, -(z_gap + hub_thickness)))
hub_R = Part.makeCylinder(hub_radius, hub_thickness, App.Vector(0, 0, axle_length + z_gap))

# Fuse the solid rings to the stand FIRST so the pipes blend into the rings
stand = stand.fuse(hub_L).fuse(hub_R)

# NOW cut the holes completely out of the resulting stand.
hub_L_hole = Part.makeCylinder(hub_hole_radius, hub_thickness + 20*scale, App.Vector(0, 0, -(z_gap + hub_thickness + 10*scale)))
hub_R_hole = Part.makeCylinder(hub_hole_radius, hub_thickness + 20*scale, App.Vector(0, 0, axle_length))

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

