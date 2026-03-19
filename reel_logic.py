import FreeCAD as App
import Part
import math
import os

doc = App.newDocument()

# --- Responsive Sizing Geometry ---
user_scale = 1.0
scale = user_scale * 0.95
clearance = 0.5 * scale  # crucial 0.5mm mechanical gap for print-in-place and snap-fitting!

# Core Spool Dimensions
flange_radius = 120 * scale
flange_thickness = 15 * scale
axle_radius = 30 * scale
axle_length = 160 * scale # Clean width specifically for winding cord
half_axle = axle_length / 2.0

pin_radius = 15 * scale
pin_length = 40 * scale   

# Fully redesigned Semi-Rectangular Flat-Pack Stand parameters
frame_width = 32 * scale     # Extra thick strut width for the stand
hub_thickness = 32 * scale   # Strut thickness perfectly matching width to form massive solid rectangular blocks
hub_radius = 50 * scale      # Expanding stand ring hub perfectly around axle
hub_hole_radius = pin_radius + 1.0 * scale # Spin gap

crossbar_radius = 12 * scale # Thicker solid circular crossbars to span between A-Frames
z_gap = 5 * scale            # Frictionless airgap between reel wheel and frame

# --- 1. Right Spool Half ---
r_flange = Part.makeCylinder(flange_radius, flange_thickness, App.Vector(0,0, half_axle))
r_axle = Part.makeCylinder(axle_radius, half_axle, App.Vector(0,0,0))

# Inner interlocking Peg
peg_radius = axle_radius - (10 * scale)
r_axle_peg = Part.makeCylinder(peg_radius, 25*scale, App.Vector(0,0,-25*scale))

# Outer Pin
r_pin = Part.makeCylinder(pin_radius, pin_length, App.Vector(0,0, half_axle + flange_thickness))

# Lighten Flange with material cutouts
hole_radius = 30 * scale
hole_dist = 70 * scale
for i in range(6):
    angle = math.radians(i * 60)
    hx = hole_dist * math.cos(angle)
    hy = hole_dist * math.sin(angle)
    cutter = Part.makeCylinder(hole_radius, flange_thickness + 10, App.Vector(hx, hy, half_axle - 5))
    r_flange = r_flange.cut(cutter)

# Socket perfectly sized for modular Handle to snap into right flange
handle_peg_radius = 8 * scale
handle_hole = Part.makeCylinder(handle_peg_radius + clearance, flange_thickness + 10, App.Vector(hole_dist, 0, half_axle - 5))
r_flange = r_flange.cut(handle_hole)

right_spool = r_flange.fuse(r_axle).fuse(r_axle_peg).fuse(r_pin)
right_spool = right_spool.removeSplitter()


# --- 2. Left Spool Half ---
l_flange = Part.makeCylinder(flange_radius, flange_thickness, App.Vector(0,0, -half_axle - flange_thickness))
l_axle = Part.makeCylinder(axle_radius, half_axle, App.Vector(0,0,-half_axle))

# Inner interlocking Hole with clearance so it slides onto Right half effortlessly
l_axle_hole = Part.makeCylinder(peg_radius + clearance, 30*scale, App.Vector(0,0,-28*scale)) 
l_pin = Part.makeCylinder(pin_radius, pin_length, App.Vector(0,0, -half_axle - flange_thickness - pin_length))

for i in range(6):
    angle = math.radians(i * 60)
    hx = hole_dist * math.cos(angle)
    hy = hole_dist * math.sin(angle)
    cutter = Part.makeCylinder(hole_radius, flange_thickness + 10, App.Vector(hx, hy, -half_axle - flange_thickness - 5))
    l_flange = l_flange.cut(cutter)
    
left_spool = l_flange.fuse(l_axle).fuse(l_pin).cut(l_axle_hole)
left_spool = left_spool.removeSplitter()


# --- 3. Modular Handle ---
# An ergonomic handle that locks straight into the slot on the right flange.
# Made slightly thicker and positioned externally
# Starts directly off the external side of right flange:
h_z = half_axle + flange_thickness 
h_peg = Part.makeCylinder(handle_peg_radius, flange_thickness, App.Vector(hole_dist, 0, h_z - flange_thickness))
h_shield = Part.makeCylinder(22*scale, 8*scale, App.Vector(hole_dist, 0, h_z)) 
h_grip = Part.makeCylinder(14*scale, 65*scale, App.Vector(hole_dist, 0, h_z + 8*scale))
handle = h_peg.fuse(h_shield).fuse(h_grip).removeSplitter()


# --- 4 & 5. Left & Right Semi-Rectangular Stand A-Frames ---
# Instead of skinny round pipes, this uses flat box framing with massive bed adhesion.
z_R = half_axle + flange_thickness + z_gap + hub_thickness/2
z_L = -half_axle - flange_thickness - z_gap - hub_thickness/2

y_floor = -140 * scale
x_spread = 95 * scale
y_top = 160 * scale

# 3D Positioning layout maps exactly to the YX Plane translated to proper Z-Axes.
def build_frame(z_plane):
    P_hub = App.Vector(0, 0, z_plane)
    P_f = App.Vector(x_spread, y_floor, z_plane)
    P_b = App.Vector(-x_spread, y_floor, z_plane)
    P_t = App.Vector(0, y_top, z_plane)

    # Function generating flat horizontal rectangles spanning between any 2 structural points flawlessly
    def make_strut(p1, p2):
        v = p2 - p1
        L = v.Length
        box = Part.makeBox(L, frame_width, hub_thickness, App.Vector(0, -frame_width/2, -hub_thickness/2))
        c1 = Part.makeCylinder(frame_width/2, hub_thickness, App.Vector(0,0,-hub_thickness/2))
        c2 = Part.makeCylinder(frame_width/2, hub_thickness, App.Vector(L,0,-hub_thickness/2))
        strut = box.fuse(c1).fuse(c2)
        angle = math.degrees(math.atan2(v.y, v.x))
        strut.Placement = App.Placement(p1, App.Rotation(App.Vector(0,0,1), angle))
        return strut

    # Base shape fuses struts with the massive integrated ring
    s1 = make_strut(P_hub, P_f)
    s2 = make_strut(P_hub, P_b)
    s3 = make_strut(P_f, P_b)   # Base support on ground
    s4 = make_strut(P_hub, P_t) # Upright Handle extension
    ring = Part.makeCylinder(hub_radius, hub_thickness, P_hub - App.Vector(0,0,hub_thickness/2))
    frame = s1.fuse(s2).fuse(s3).fuse(s4).fuse(ring)
    
    # Machine the frictionless bearing hole so it rolls perfectly
    hole = Part.makeCylinder(hub_hole_radius, hub_thickness + 10, P_hub - App.Vector(0,0,hub_thickness/2 + 5))
    
    # Mill out exact structural connection sockets for crossbars allowing snap-fit assembly
    sock1 = Part.makeCylinder(crossbar_radius + clearance, hub_thickness + 10, P_f - App.Vector(0,0,hub_thickness/2 + 5))
    sock2 = Part.makeCylinder(crossbar_radius + clearance, hub_thickness + 10, P_b - App.Vector(0,0,hub_thickness/2 + 5))
    sock3 = Part.makeCylinder(crossbar_radius + clearance, hub_thickness + 10, P_t - App.Vector(0,0,hub_thickness/2 + 5))
    
    return frame.cut(hole).cut(sock1).cut(sock2).cut(sock3).removeSplitter()

right_frame = build_frame(z_R)
left_frame = build_frame(z_L)


# --- 6, 7, 8. Tie-Rod Crossbars ---
# Designed exactly identical lengths to safely span left to right side
bar_len = (z_R + hub_thickness/2) - (z_L - hub_thickness/2)
z_origin = z_L - hub_thickness/2

bar1 = Part.makeCylinder(crossbar_radius, bar_len, App.Vector(x_spread, y_floor, z_origin))
bar2 = Part.makeCylinder(crossbar_radius, bar_len, App.Vector(-x_spread, y_floor, z_origin))
bar3 = Part.makeCylinder(crossbar_radius, bar_len, App.Vector(0, y_top, z_origin))


# --- 9 & 10. End Caps ---
# External locks that friction-fit or glue over the extreme ends to secure stand
cap_thickness = 10 * scale
cap_rad = pin_radius + 12 * scale

cap_R = Part.makeCylinder(cap_rad, cap_thickness, App.Vector(0,0, half_axle + flange_thickness + pin_length - cap_thickness))
c_R_sock = Part.makeCylinder(pin_radius + clearance, cap_thickness - 3*scale, App.Vector(0,0, half_axle + flange_thickness + pin_length - cap_thickness))
cap_R = cap_R.cut(c_R_sock)

cap_L = Part.makeCylinder(cap_rad, cap_thickness, App.Vector(0,0, -half_axle - flange_thickness - pin_length))
c_L_sock = Part.makeCylinder(pin_radius + clearance, cap_thickness - 3*scale, App.Vector(0,0, -half_axle - flange_thickness - pin_length + 3*scale))
cap_L = cap_L.cut(c_L_sock)


# Assemble logic for hierarchy
assembly = Part.makeCompound([right_spool, left_spool, handle, right_frame, left_frame, bar1, bar2, bar3, cap_R, cap_L])

# File Export handling (Individual STLs completely flat-pack ready)
export_dir = "/Users/intelligentmachine/Documents/workspace/3d-models/cord-storage-reel-v3/exports"
if not os.path.exists(export_dir):
    os.makedirs(export_dir)

right_spool.exportStl(os.path.join(export_dir, "01_Right_Spool_Half.stl"))
left_spool.exportStl(os.path.join(export_dir, "02_Left_Spool_Half.stl"))
left_frame.exportStl(os.path.join(export_dir, "03_Left_Stand_Frame.stl"))
right_frame.exportStl(os.path.join(export_dir, "04_Right_Stand_Frame.stl"))
handle.exportStl(os.path.join(export_dir, "05_Handle.stl"))
bar1.exportStl(os.path.join(export_dir, "06_Crossbar_Front.stl"))
bar2.exportStl(os.path.join(export_dir, "07_Crossbar_Back.stl"))
bar3.exportStl(os.path.join(export_dir, "08_Crossbar_TopHandle.stl"))
cap_R.exportStl(os.path.join(export_dir, "09_Locking_Cap_R.stl"))
cap_L.exportStl(os.path.join(export_dir, "10_Locking_Cap_L.stl"))

# Full Step Export
assembly.exportStep(os.path.join(export_dir, "00_Full_Assembly_Preview.step"))

print(f"\nSUCCESS! Overhauled geometry to modern semi-rectangular flat-pack.")
print(f"Generated 10 individual tool-ready STL files saved in '{export_dir}'")

