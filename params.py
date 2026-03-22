import os

# params.py

# This ratio ensures the largest printable part fits within a 250 mm build
# volume when user_scale = 1.0.
user_scale = 1.0
scale = user_scale * (250.0 / 332.0)
clearance = 0.5 * scale

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
EXPORT_DIR = os.path.join(PROJECT_DIR, "exports")

# Core Spool
flange_radius = 120 * scale
flange_thickness = 15 * scale
axle_radius = 30 * scale
axle_length = 160 * scale
half_axle = axle_length / 2.0

pin_radius = axle_radius
# Stand parameters
frame_width = 32 * scale     
hub_thickness = 32 * scale   
hub_radius = 50 * scale      
hub_hole_radius = pin_radius + 2.0 * scale 

crossbar_radius = 12 * scale 
z_gap = 5 * scale            

cap_depth = 7 * scale
right_axle_pin_length = z_gap + hub_thickness
handle_standoff = 6 * scale
handle_peg_length = handle_standoff + 10 * scale + cap_depth
right_pin_length = right_axle_pin_length + handle_peg_length
left_pin_length = z_gap + hub_thickness + cap_depth

# Spool Cutouts & Pegs
hole_radius = 30 * scale
hole_dist = 70 * scale
handle_peg_radius = 12 * scale
peg_radius = axle_radius - (10 * scale)

# Absolute Z planes for the frame structures
z_R = half_axle + flange_thickness + z_gap + hub_thickness/2
z_L = -half_axle - flange_thickness - z_gap - hub_thickness/2

y_floor = -140 * scale
x_spread = 95 * scale
y_top = 160 * scale

# Handle mounting coordinates on the right spool axle peg
right_frame_outer_z = z_R + hub_thickness / 2.0
frame_handle_mount_x = 0.0
frame_handle_mount_y = 0.0
