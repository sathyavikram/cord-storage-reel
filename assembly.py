import FreeCAD as App
import Part
import os
import sys
import importlib

# Ensure the local directory is in the python path to import the split modules
_script_dir = os.path.dirname(os.path.abspath(__file__))
if _script_dir not in sys.path:
    sys.path.insert(0, _script_dir)

import part_01_spool_right
import part_01_spool_left
import part_02_handle
import part_03_frame
import part_04_crossbars
import part_05_caps

importlib.reload(part_01_spool_right)
importlib.reload(part_01_spool_left)
importlib.reload(part_02_handle)
importlib.reload(part_03_frame)
importlib.reload(part_04_crossbars)
importlib.reload(part_05_caps)

from part_01_spool_right import build_right_spool
from part_01_spool_left import build_left_spool
from part_02_handle import build_handle
from part_03_frame import build_right_frame, build_left_frame
from part_04_crossbars import build_crossbars
from part_05_caps import build_caps


def get_export_dir():
    return os.path.join(_script_dir, "exports", "assembly")

def generate_assembly():
    doc = App.newDocument("ReelAssembly")

    print("Generating Spools...")
    right_spool = build_right_spool()
    left_spool = build_left_spool()
    
    print("Generating Handle...")
    handle = build_handle()
    
    print("Generating Frames...")
    right_frame = build_right_frame()
    left_frame = build_left_frame()
    
    print("Generating Crossbars...")
    bar1, bar2, bar3 = build_crossbars()
    
    print("Generating Caps...")
    cap_R, cap_L = build_caps()

    print("Constructing Assembly...")
    assembly = Part.makeCompound([
        right_spool, left_spool, handle, 
        right_frame, left_frame, 
        bar1, bar2, bar3, 
        cap_R, cap_L
    ])

    obj = doc.addObject("Part::Feature", "Reel_Assembly")
    obj.Shape = assembly

    export_dir = get_export_dir()
    if not os.path.exists(export_dir):
        os.makedirs(export_dir)

    print(f"Exporting files to {export_dir}...")
    right_spool.exportStl(os.path.join(export_dir, "01_Spool_Right.stl"))
    left_spool.exportStl(os.path.join(export_dir, "01_Spool_Left.stl"))
    handle.exportStl(os.path.join(export_dir, "02_Handle.stl"))
    left_frame.exportStl(os.path.join(export_dir, "03_Frame_Left.stl"))
    right_frame.exportStl(os.path.join(export_dir, "03_Frame_Right.stl"))
    bar1.exportStl(os.path.join(export_dir, "04_Crossbar_Front.stl"))
    bar2.exportStl(os.path.join(export_dir, "04_Crossbar_Back.stl"))
    bar3.exportStl(os.path.join(export_dir, "04_Crossbar_Top.stl"))
    cap_R.exportStl(os.path.join(export_dir, "05_Cap_R.stl"))
    cap_L.exportStl(os.path.join(export_dir, "05_Cap_L.stl"))

    assembly.exportStep(os.path.join(export_dir, "00_Full_Assembly_Preview.step"))
    print("Generation complete!")

if __name__ == "__main__":
    generate_assembly()
