# 🧵 Heavy-Duty Cord Storage Reel (Modular 3D Printable)

A fully parametric, modular, and support-free 3D printable cord storage reel. Designed using FreeCAD's Python API through Constructive Solid Geometry (CSG), this project generates a sturdy 10-piece "flat-pack" assembly that seamlessly snaps together.

At its default scale (`user_scale = 1.0`), the largest printable part fits inside a standard **250x250x250 mm** 3D printer build volume and the assembled reel can hold about **~105 feet of 14/3 wire**.

## ✨ Features
* **Modular, Print-Friendly Parts:** The reel breaks down into simple printable parts (frames, crossbars, split spool, handle, caps) for reliable slicing and straightforward assembly. Included print profiles (`3d-print/` folder) for Bambu and Creality.
* **Fully Parametric:** Just change the `user_scale` variable in `params.py` to proportionally shrink or enlarge the entire assembly. Clearances and tolerances scale automatically.
* **Slip-Fit & Threaded Assembly:** Features center spool alignment, a dedicated handle peg, press-fit crossbars, and retaining threaded parts (fasteners and caps) with mathematically calculated tolerances, including extra clearance (`0.4 mm * scale`) for easy rotation.
* **Auto-Exporting:** Running the scripts generates `.step` and `.stl` files directly into the local `exports/` folder.
* **Rich Media:** See the `media/` folder in the project for visual references, assembly videos, and reference images.

## 📂 File Architecture
The monolithic code has been separated out for easier maintenance and independent part generation:

* `params.py` - Global configuration (scale, dimensions, clearances).
* `part_01_spool_left.py` - Inner rotating spool (Left Half, containing female connector socket).
* `part_01_spool_right.py` - Inner rotating spool (Right Half, containing the stepped axle pin and handle peg).
* `part_02_handle.py` - Hand crank that mounts on the exposed right spool axle peg.
* `part_03_frame.py` - Heavy-duty A-frame structural sides with round crossbar sockets.
* `part_04_crossbars.py` - Cylindrical crossbars that connect the two frame sides.
* `part_04_fasteners.py` - Threaded fasteners with deep screwdriver slots (4.5mm) for structural assembly.
* `part_05_caps.py` - Retaining caps that lock the rotating spool onto the frame.
* `assembly.py` - Master script that imports all parts, constructs the full digital assembly, and exports everything.

## 🚀 How to Generate the 3D Models

### Method 1: Using FreeCAD GUI (Recommended)
1. Open FreeCAD.
2. Open the Python Console (`View` > `Panels` > `Python console`).
3. Open any of the project Python scripts from this folder in the FreeCAD editor so relative imports resolve from the project directory.
4. Execute the script. 
5. The part(s) will be visually rendered in your 3D view, and the `.stl` and `.step` files will be written to the project's `exports/` directory.

### Method 2: Headless CLI (Mac / Linux)
If your terminal's Python environment knows where the FreeCAD `lib` directory is, you can run it directly from your terminal:

```bash
# Example for macOS: Add FreeCAD to your python path and run the assembly
python3 -c "import sys; sys.path.append('/Applications/FreeCAD.app/Contents/Resources/lib'); import assembly; assembly.generate_assembly()"
```

## 📐 Customizing the Scale & Capacity

Want to print a smaller reel for Paracord? Or a massive one for hoses? 
1. Open `params.py`
2. Change the `user_scale` variable (Default is `1.0`).

Estimated capacities at about 70% packing efficiency:

| `user_scale` | Minimum Build Plate Required | Capacity (14/3 Cord, ~9 mm) | Capacity (16/3 Cord, ~8 mm) |
|------------|-----------------------------|-----------------------------|-----------------------------|
| 0.50       | 125 mm x 125 mm x 125 mm     | **~13 feet**                | **~16 feet**                |
| 0.75       | 187 mm x 187 mm x 187 mm     | **~44 feet**                | **~56 feet**                |
| **1.00**   | **250 mm x 250 mm x 250 mm** | **~105 feet**               | **~132 feet**               |
| 1.25       | 315 mm x 315 mm x 315 mm     | **~205 feet**               | **~258 feet**               |
| 1.50       | 375 mm x 375 mm x 375 mm     | **~353 feet**               | **~447 feet**               |
| 2.00       | 500 mm x 500 mm x 500 mm     | **~838 feet**               | **~1,060 feet**             |

*At `user_scale = 1.0`, the scaling is tuned so the largest single printable part stays within a 250 mm build envelope. The full digital assembly preview is larger than that because it shows the reel already assembled.*

## 🔧 Assembly Instructions

**Preparation:** Ensure all support material (if any) is removed and the mating surfaces are clean. Test-fit the parts before applying any glue.

1. **Assemble the Spool:** Align and press the **Left Spool Half** (`01_Spool_Left.stl`) and **Right Spool Half** (`01_Spool_Right.stl`) together using the center locking peg.
2. **Mount the Frames:** Slide the **Left Frame** (`03_Frame_Left.stl`) and **Right Frame** (`03_Frame_Right.stl`) onto the protruding axles of the fully assembled spool.
3. **Install the Crossbars:** With the frames seated on the spool axles, press the **3 Crossbars** (`04_Crossbar_Front.stl`, `04_Crossbar_Back.stl`, `04_Crossbar_Top.stl`) into the round sockets between the two frames to lock the main structure together. Add CA glue or epoxy to the crossbar sockets if you want a permanent frame.
4. **Attach the Handle:** Slip the **Handle** (`02_Handle.stl`) outer socket over the smaller, outermost handle peg extending from the **Right Spool** axle. 
5. **Lock it Together:** Snap or glue the **Caps** (`05_Cap_L.stl` and `05_Cap_R.stl`) onto the extremely exposed pin ends (one cap on the far left of the spool axle, one cap holding the handle onto the right peg) to securely retain the moving parts.