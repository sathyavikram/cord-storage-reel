import sys, os
sys.path.append('/Applications/FreeCAD.app/Contents/Resources/lib')
import FreeCAD as App
import Part
import math
import part_01_spool_right

spool = part_01_spool_right.build_right_spool()
print("Right spool volume:", spool.Volume)
print("Right spool bounding box:", spool.BoundBox)
