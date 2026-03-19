# params.py
user_scale = 1.0
scale = user_scale * 0.95
clearance = 0.5 * scale

# Core Spool
flange_radius = 120 * scale
flange_thickness = 15 * scale
axle_radius = 30 * scale
axle_length = 160 * scale
half_axle = axle_length / 2.0

pin_radius = 15 * scale
pin_length = 40 * scale   

# Stand parameters
frame_width = 32 * scale     
hub_thickness = 32 * scale   
hub_radius = 50 * scale      
hub_hole_radius = pin_radius + 1.0 * scale 

crossbar_radius = 12 * scale 
z_gap = 5 * scale            

# Spool Cutouts & Pegs
hole_radius = 30 * scale
hole_dist = 70 * scale
handle_peg_radius = 8 * scale
peg_radius = axle_radius - (10 * scale)

# Absolute Z planes for the frame structures
z_R = half_axle + flange_thickness + z_gap + hub_thickness/2
z_L = -half_axle - flange_thickness - z_gap - hub_thickness/2

y_floor = -140 * scale
x_spread = 95 * scale
y_top = 160 * scale
