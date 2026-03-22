import FreeCAD as App
import Part
import sys
import os

try:
    _script_dir = os.path.dirname(os.path.abspath(__file__))
except NameError:
    _script_dir = os.getcwd()
if _script_dir not in sys.path:
    sys.path.insert(0, _script_dir)

if "params" in sys.modules: del sys.modules["params"]
from params import *
from part_01_spool_right import build_right_spool

def generate_right_peg_test():
    """Extracts only the snap-fit peg from the Right Spool to test printer tolerances."""
    
    # Generate the whole spool
    full_spool = build_right_spool()
    
    # We only care about the peg tip and part of the hex.
    # The hex peg goes from Z = -25 to 0. The integrated anchor goes from Z = -50 to -25.
    # A box spanning from Z=-55 to Z=-10 gives us the anchor plus 15mm of hex to grab.
    
    box_size = 60 * scale
    # Box origin: centered in X/Y, Z from -55
    bounding_box = Part.makeBox(box_size, box_size, 45 * scale, 
                                App.Vector(-box_size/2, -box_size/2, -55 * scale))
                                
    # Intersect to extract ONLY what's inside the box
    test_peg = full_spool.common(bounding_box)
    return test_peg

if __name__ == '__main__':
    doc_name = "ToleranceTest_RightPeg"
    try:
        doc = App.getDocument(doc_name)
    except Exception:
        doc = None
    if doc is not None:
        for obj in doc.Objects:
            doc.removeObject(obj.Name)
    else:
        doc = App.newDocument(doc_name)

    test_part = generate_right_peg_test()
    Part.show(test_part, 'Right_Peg_Test')
    
    export_dir = os.path.join(EXPORT_DIR, 'test_prints')
    os.makedirs(export_dir, exist_ok=True)
    out_path = os.path.join(export_dir, 'Test_Right_Peg.stl')
    print(f"Exporting Right Peg Test to {out_path}")
    test_part.exportStl(out_path)
