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
from part_01_spool_left import build_left_spool

def generate_left_socket_test():
    """Extracts only the snap-fit socket from the Left Spool to test printer tolerances."""
    
    # Generate the whole spool
    full_spool = build_left_spool()
    
    # The left female hole exists deep in the axle. 
    # The hex hole goes to Z=-26. The anchor ribs extend from Z = -52 up to Z = -26.
    # A box spanning from Z=-55 to Z=-15 gives us the ribbed ribs plus 11mm of the hex.
    
    box_size = 60 * scale
    bounding_box = Part.makeBox(box_size, box_size, 40 * scale, 
                                App.Vector(-box_size/2, -box_size/2, -55 * scale))
                                
    # Intersect to extract ONLY what's inside the box
    test_socket = full_spool.common(bounding_box)
    
    # Optional: Cut the exterior of the extracted block so it's not a massive solid square
    # We want it to be a relatively thin-walled cylinder around the hole simulating real print behavior
    outer_cut = Part.makeCylinder(axle_radius + (5 * scale), 50 * scale, App.Vector(0,0,-60*scale))
    test_socket = test_socket.common(outer_cut)
    
    return test_socket

if __name__ == '__main__':
    doc_name = "ToleranceTest_LeftSocket"
    try:
        doc = App.getDocument(doc_name)
    except Exception:
        doc = None
    if doc is not None:
        for obj in doc.Objects:
            doc.removeObject(obj.Name)
    else:
        doc = App.newDocument(doc_name)

    test_part = generate_left_socket_test()
    Part.show(test_part, 'Left_Socket_Test')
    
    export_dir = os.path.join(EXPORT_DIR, 'test_prints')
    os.makedirs(export_dir, exist_ok=True)
    out_path = os.path.join(export_dir, 'Test_Left_Socket.stl')
    print(f"Exporting Left Socket Test to {out_path}")
    test_part.exportStl(out_path)
