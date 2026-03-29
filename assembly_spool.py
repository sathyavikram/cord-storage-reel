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

def create_spool_assembly():
    doc_name = "SpoolAssembly"
    try:
        doc = App.getDocument(doc_name)
    except Exception:
        doc = App.newDocument(doc_name)
    
    for obj in doc.Objects:
        doc.removeObject(obj.Name)

    exports_dir = os.path.join(_script_dir, "exports")
    
    generation_map = {
        "part_01_spool_left.step": part_01_spool_left.build_left_spool,
        "part_01_spool_right.step": part_01_spool_right.build_right_spool
    }

    parts_to_import = [
        "part_01_spool_left.step",
        "part_01_spool_right.step"
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
    assembly_obj = doc.addObject("Part::Feature", "Spool_Assembly_Group")
    assembly_obj.Shape = compound_shape
    
    doc.recompute()
    
    assembly_export_path = os.path.join(exports_dir, "00_Spool_Assembly_Preview.step")
    if os.path.exists(assembly_export_path):
        os.remove(assembly_export_path)
    
    compound_shape.exportStep(assembly_export_path)
    print("Assembly complete.")

if __name__ == "__main__":
    create_spool_assembly()