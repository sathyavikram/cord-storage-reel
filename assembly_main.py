import FreeCAD as App
import Import
import Part
import os
import sys

_script_dir = os.path.dirname(os.path.abspath(__file__))
if _script_dir not in sys.path:
    sys.path.insert(0, _script_dir)

import part_01_spool_right
import part_01_spool_left
import part_02_handle
import part_03_frame
import part_04_crossbars
import part_05_caps
import part_01_center_bolt
import part_04_fasteners

# Re-import params so we can place frames and crossbars perfectly
from params import z_R, z_L, x_spread, y_floor, y_top

def get_export_dir():
    _script_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(_script_dir, "exports")

def generate_assembly():
    doc_name = "ReelAssembly"
    try:
        doc = App.getDocument(doc_name)
    except Exception:
        doc = None

    if doc is not None:
        for obj in doc.Objects:
            doc.removeObject(obj.Name)
    else:
        doc = App.newDocument(doc_name)

    export_dir = get_export_dir()
    
    # We map logical assembly components to their standardized source step files and apply specific placements
    components = [
        {"name": "Spool Right", "file": "part_01_spool_right.step", "pos": App.Placement(), "gen": part_01_spool_right.build_right_spool},
        {"name": "Spool Left", "file": "part_01_spool_left.step", "pos": App.Placement(), "gen": part_01_spool_left.build_left_spool},
        {"name": "Handle", "file": "part_02_handle.step", "pos": App.Placement(), "gen": part_02_handle.build_handle},
        {"name": "Frame Right", "file": "part_03_frame.step", "pos": App.Placement(App.Vector(0,0,z_R), App.Rotation()), "gen": part_03_frame.build_frame_export},
        {"name": "Frame Left", "file": "part_03_frame.step", "pos": App.Placement(App.Vector(0,0,-z_R), App.Rotation(App.Vector(0,1,0), 180)), "gen": part_03_frame.build_frame_export},
        {"name": "Crossbar Front", "file": "part_04_crossbars.step", "pos": App.Placement(App.Vector(x_spread, y_floor, 0), App.Rotation()), "gen": part_04_crossbars.build_crossbars_export},
        {"name": "Crossbar Back", "file": "part_04_crossbars.step", "pos": App.Placement(App.Vector(-x_spread, y_floor, 0), App.Rotation()), "gen": part_04_crossbars.build_crossbars_export},
        {"name": "Crossbar Top", "file": "part_04_crossbars.step", "pos": App.Placement(App.Vector(0, y_top, 0), App.Rotation()), "gen": part_04_crossbars.build_crossbars_export},
        {"name": "Cap Left", "file": "part_05_caps.step", "pos": App.Placement(), "gen": part_05_caps.build_caps},
        {"name": "Center Bolt", "file": "part_01_center_bolt.step", "pos": App.Placement(), "gen": part_01_center_bolt.build_printed_bolt},
        {"name": "Frame Bolt", "file": "part_04_fasteners.step", "pos": App.Placement(), "gen": part_04_fasteners.build_fastener}
    ]

    assembly_parts = []
    
    print("Importing components for assembly preview...")
    for comp in components:
        filepath = os.path.join(export_dir, comp["file"])
        
        # Auto-generation
        if not os.path.exists(filepath):
            print(f"File not found: {comp['file']}. Generating it now...")
            if comp["gen"]:
                comp["gen"]()
            else:
                print(f"Warning: No generation function mapped for {comp['file']}")
        
        if os.path.exists(filepath):
            print(f"Importing {comp['name']} from {comp['file']}...")
            Import.insert(filepath, doc.Name)
            inserted_obj = doc.Objects[-1]
            shape = inserted_obj.Shape.copy()
            
            # Apply transformation
            shape.Placement = comp["pos"].multiply(shape.Placement)
            assembly_parts.append(shape)
            
            doc.removeObject(inserted_obj.Name)
        else:
            print(f"Warning: Failed to load: {filepath}")

    if not assembly_parts:
        print("Required part files were not found.")
        return

    print("Constructing Assembly...")
    assembly = Part.makeCompound(assembly_parts)

    obj = doc.addObject("Part::Feature", "Reel_Assembly")
    obj.Shape = assembly

    print(f"Exporting assembly files to {export_dir}...")
    assembly.exportStep(os.path.join(export_dir, "assembly_main.step"))
    assembly.exportStl(os.path.join(export_dir, "00_Full_Assembly_Preview.stl"))
    print("Generation complete!")

if __name__ == "__main__":
    generate_assembly()
