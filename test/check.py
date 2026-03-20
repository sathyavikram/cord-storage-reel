import sys
import os

_script_dir = "/Users/intelligentmachine/Documents/workspace/3d-models/cord-storage-reel-v3"
if _script_dir not in sys.path:
    sys.path.insert(0, _script_dir)

from part_03_frame import build_right_frame
import FreeCAD as App
import Part

doc = App.newDocument('test_frame')
obj = doc.addObject("Part::Feature", "Right_Frame")
obj.Shape = build_right_frame()
