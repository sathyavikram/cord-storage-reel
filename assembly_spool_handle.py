import FreeCAD as App
import Import
import Part
import os
import sys

_script_dir = os.path.dirname(os.path.abspath(__file__))
if _script_dir not in sys.path:
    sys.path.insert(0, _script_dir)

import part_01_spool_left
import part_01_spool_right
import part_02_handle
import importlib
importlib.reload(part_01_spool_left)
importlib.reload(part_01_spool_right)
importlib.reload(part_02_handle)

def create_spool_handle_assembly():
    doc_name = "SpoolHandleAssembly"
    try:
        doc = App.getDocument(doc_name)
    except Exception:
        doc = App.newDocument(doc_name)
    
    for obj in doc.Objects:
        doc.removeObject(obj.Name)

    exports_dir = os.path.join(_script_dir, "exports")
    
    generation_map = {
        "part_01_spool_left.step": part_01_spool_left.build_left_spool,
        "part_01_spool_right.step": part_01_spool_right.build_right_spool,
        "part_02_handle.step": part_02_handle.build_handle
    }

    parts_to_import = [
        "part_01_spool_left.step",
        "part_01_spool_right.step",
        "part_02_handle.step"
    ]
    
    assembly_parts = []
    
    for filename in parts_to_import:
        filepath = os.path.join(exports_dir, filename)
        if not os.path.exists(filepath):
            if filename in generation_map:
                generation_map[filename]()
        
        if os.path.exists(filepath):
            Import.insert(filepath, doc.Name)
            inserted_obj = doc.Objects[-1]
            assembly_parts.append(inserted_obj.Shape)

    if not assembly_parts:
        return

    compound_shape = Part.makeCompound(assembly_parts)
    assembly_obj = doc.addObject("Part::Feature", "Spool_Handle_Assembly_Group")
    assembly_obj.Shape = compound_shape
    
    doc.recompute()
    
    assembly_export_step = os.path.join(exports_dir, "assembly_spool_handle.step")
    assembly_export_stl = os.path.join(exports_dir, "assembly_spool_handle.stl")
    
    for path in [assembly_export_step, assembly_export_stl]:
        if os.path.exists(path):
            os.remove(path)
    
    compound_shape.exportStep(assembly_export_step)
    compound_shape.exportStl(assembly_export_stl)
    print("Spool and Handle assembly complete.")

if __name__ == "__main__":
    create_spool_handle_assembly()
