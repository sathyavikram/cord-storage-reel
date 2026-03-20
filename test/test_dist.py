import sys, os
_script_dir = "/Users/intelligentmachine/Documents/workspace/3d-models/cord-storage-reel-v3"
if _script_dir not in sys.path:
    sys.path.insert(0, _script_dir)
from part_01_spool_right import build_right_spool
from part_02_handle import build_handle
from part_05_caps import build_caps

right_spool = build_right_spool()
handle = build_handle()
cap_R, _ = build_caps()

d_handle_spool = handle.distToShape(right_spool)[0]
d_handle_cap = handle.distToShape(cap_R)[0]

s = f"Handle -> Spool: {d_handle_spool:.4f} mm\nHandle -> Cap_R: {d_handle_cap:.4f} mm\n"
with open("/Users/intelligentmachine/Documents/workspace/3d-models/cord-storage-reel-v3/dist.txt", "w") as f:
    f.write(s)

import FreeCAD as App
import Part
doc = App.newDocument('test')
Part.show(Part.makeBox(1,1,1))
