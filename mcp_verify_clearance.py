import FreeCAD as App
import Part
import sys, os

# Ensure modules can be imported
_script_dir = os.path.dirname(os.path.abspath(__file__))
if _script_dir not in sys.path:
    sys.path.insert(0, _script_dir)

from part_01_spool_left import build_left_spool
from part_03_frame import build_frame
from params import *

doc = App.ActiveDocument
if doc is None:
    doc = App.newDocument('VerifyClearance')

spool = build_left_spool()
frame_left = build_frame(z_L, is_left=True)

s_obj = doc.addObject("Part::Feature", "Spool")
s_obj.Shape = spool

f_obj = doc.addObject("Part::Feature", "Frame")
f_obj.Shape = frame_left

# Add a close-up camera view around the left frame hub
App.ActiveDocument.recompute()
