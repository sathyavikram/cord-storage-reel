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
import importlib
for mod in [part_01_spool_right, part_01_spool_left, part_02_handle, part_03_frame, part_04_crossbars, part_05_caps, part_01_center_bolt, part_04_fasteners]:
    importlib.reload(mod)

# Re-import params so we can place frames and crossbars perfectly
from params import z_R, z_L, x_spread, y_floor, y_top, hub_thickness

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
    
    # Pre-calculated Z values and rotations for fasteners
    z_right_outer = z_R + hub_thickness / 2
    z_left_outer = z_L - hub_thickness / 2
    bolt_rot_R = App.Rotation(App.Vector(1,0,0), 180) # Face -Z
    bolt_rot_L = App.Rotation() # Face +Z

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
        # Right Fasteners
        {"name": "Frame Bolt R1", "file": "part_04_fasteners.step", "pos": App.Placement(App.Vector(x_spread, y_floor, z_right_outer), bolt_rot_R), "gen": part_04_fasteners.build_fastener},
        {"name": "Frame Bolt R2", "file": "part_04_fasteners.step", "pos": App.Placement(App.Vector(-x_spread, y_floor, z_right_outer), bolt_rot_R), "gen": part_04_fasteners.build_fastener},
        {"name": "Frame Bolt R3", "file": "part_04_fasteners.step", "pos": App.Placement(App.Vector(0, y_top, z_right_outer), bolt_rot_R), "gen": part_04_fasteners.build_fastener},
        # Left Fasteners
        {"name": "Frame Bolt L1", "file": "part_04_fasteners.step", "pos": App.Placement(App.Vector(x_spread, y_floor, z_left_outer), bolt_rot_L), "gen": part_04_fasteners.build_fastener},
        {"name": "Frame Bolt L2", "file": "part_04_fasteners.step", "pos": App.Placement(App.Vector(-x_spread, y_floor, z_left_outer), bolt_rot_L), "gen": part_04_fasteners.build_fastener},
        {"name": "Frame Bolt L3", "file": "part_04_fasteners.step", "pos": App.Placement(App.Vector(0, y_top, z_left_outer), bolt_rot_L), "gen": part_04_fasteners.build_fastener}
    ]

    assembly_parts = []
    assembly_objs = []
    
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
            shape = Part.Shape()
            shape.read(filepath)
            
            # Apply transformation
            shape.Placement = comp["pos"].multiply(shape.Placement)
            assembly_parts.append(shape)
            
            # Create a named feature for the STEP tree
            part_name = comp["name"].replace(" ", "_").replace("-", "_")
            feat = doc.addObject("Part::Feature", part_name)
            feat.Label = comp["name"]  # This label determines what Fusion 360 shows
            feat.Shape = shape
            assembly_objs.append(feat)
        else:
            print(f"Warning: Failed to load: {filepath}")

    if not assembly_parts:
        print("Required part files were not found.")
        return

    print("Constructing Assembly...")
    assembly = Part.makeCompound(assembly_parts)

    print(f"Exporting assembly files to {export_dir}...")
    
    # FreeCAD requires objects to be part of the active document and recomputed before STEP export
    # Unlinked shapes or uncomputed features usually export as 0 bytes or throw warnings.
    doc.recompute()
    
    # Export the individual objects as a multi-body STEP file
    step_file_path = os.path.join(export_dir, "assembly_main.step")
    if os.path.exists(step_file_path):
        os.remove(step_file_path)
    Import.export(assembly_objs, step_file_path)
    
    # Export the combined compound as a single STL
    stl_file_path = os.path.join(export_dir, "assembly_main.stl")
    if os.path.exists(stl_file_path):
        os.remove(stl_file_path)
    assembly.exportStl(stl_file_path)
    print("Generation complete!")

if __name__ == "__main__":
    generate_assembly()
