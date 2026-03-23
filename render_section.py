import sys, os
import FreeCAD as App
import Part

script_dir = "/Users/intelligentmachine/Documents/workspace/3d-models/cord-storage-reel-v3"
if script_dir not in sys.path:
    sys.path.insert(0, script_dir)

from assembly import build_right_spool, build_left_spool, build_handle, build_right_frame, build_left_frame, build_crossbars, build_caps

rs = build_right_spool()
ls = build_left_spool()
h = build_handle()
rf = build_right_frame()
lf = build_left_frame()
c1, c2, c3 = build_crossbars()
_, cl = build_caps()

# Combine all parts
parts = [rs, ls, h, rf, lf, c1, c2, c3, cl]
assembly_shape = Part.makeCompound(parts)

# Create a cutting box to remove one half (remove y > 0)
# The Z-axis is the axle. Cutting Y > 0 will split the model down the middle of the axle.
cut_box = Part.makeBox(400, 400, 400, App.Vector(-200, 0, -200))
section = assembly_shape.cut(cut_box)

doc = App.newDocument("SectionDoc")
obj = doc.addObject("Part::Feature", "CrossSection")
obj.Shape = section
