import FreeCAD as App
import Part
import os
import sys

# Ensure the local directory is in the python path to import the split modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from part_01_spool_right import build_right_spool
from part_01_spool_left import build_left_spool
from part_02_handle import build_handle
from part_03_frame import build_right_frame, build_left_frame
from part_04_crossbars import build_crossbars
from part_05_caps import build_caps

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

    export_dir = "/Users/intelligentmachine/Documents/workspace/3d-models/cord-storage-reel-v3/exports"
    if not os.path.exists(export_dir):
        os.makedirs(export_dir)

    print(f"Exporting files to {export_dir}...")
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

    assembly.exportStep(os.path.join(export_dir, "00_Full_Assembly_Preview.step"))
    print("Generation complete!")

if __name__ == "__main__":
    generate_assembly()
