import sys, os
_script_dir = "/Users/intelligentmachine/Documents/workspace/3d-models/cord-storage-reel-v3"
sys.path.insert(0, _script_dir)
from part_02_handle import build_handle
h = build_handle()
print("Handle bounding box:", h.BoundBox)
