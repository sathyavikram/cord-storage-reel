import sys, os
sys.path.append('/Applications/FreeCAD.app/Contents/Resources/lib')
import FreeCAD as App
import Part

try:
    thread = Part.makeThread(2.0, 1.0, 10.0, 10.0)
    print("makeThread BoundBox:", thread.BoundBox)
except Exception as e:
    print(e)
