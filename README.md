# 🧵 Heavy-Duty Cord Storage Reel (Modular 3D Printable)

A fully parametric, modular, and support-free 3D printable cord storage reel. Designed using FreeCAD's Python API through Constructive Solid Geometry (CSG), this project generates a sturdy 10-piece "flat-pack" assembly that seamlessly snaps together.

At its default scale (`user_scale = 1.0`), the reel perfectly fits inside a standard **250x250x250mm** 3D printer build volume and can hold up to **~150 feet of 14/3 Gauge Wire**.

## ✨ Features
* **Zero Supports Needed:** The flat-pack modular design breaks down complex geometries into print-flat pieces (frames, crossbars, split spool), ensuring minimal waste and fast print times.
* **Fully Parametric:** Just change the `user_scale` variable in `params.py` to proportionally shrink or enlarge the entire assembly. Clearances and tolerances scale automatically.
* **Snap-Fit Architecture:** Features precise locking pin joints, peg connections, and handle bearings with mathematically calculated tolerances (`0.5mm * scale`).
* **Auto-Exporting:** Running the scripts automatically generates `.step` and `.stl` files directly into an `exports/` folder.

## 📂 File Architecture
The monolithic code has been separated out for easier maintenance and independent part generation:

* `params.py` - Global configuration (scale, dimensions, clearances).
* `part_01_spool_left.py` - Inner rotating spool (Left Half, containing female connector socket).
* `part_01_spool_right.py` - Inner rotating spool (Right Half, containing peg and handle mount).
* `part_02_handle.py` - Rotating hand crank grip and shield.
* `part_03_frame.py` - Heavy-duty A-Frame structural sides with hex-cutouts.
* `part_04_crossbars.py` - Cylindrical crossbars that connect the two A-Frames.
* `part_05_caps.py` - Locking caps that hold the rotating axle onto the frame.
* `assembly.py` - Master script that imports all parts, constructs the full digital assembly, and exports everything.

## 🚀 How to Generate the 3D Models

### Method 1: Using FreeCAD GUI (Recommended)
1. Open FreeCAD.
2. Open the Python Console (`View` > `Panels` > `Python console`).
3. Open any of the python scripts in the FreeCAD text editor or copy-paste their contents into the console.
4. Execute the script. 
5. The part(s) will be visually rendered in your 3D view, and the `.stl` and `.step` files completely be automatically deposited into the `exports/` directory.

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

Estimated Capacities for 9mm diameter cord (14/3 gauge) at ~70% packing efficiency:
* `user_scale = 0.50` (Max Frame Width 125mm): **~18 feet** 
* `user_scale = 0.75` (Max Frame Width 187mm): **~60 feet**
* `user_scale = 1.00` (Max Frame Width 250mm): **~142 feet**
* `user_scale = 1.25` (Max Frame Width 312mm): **~277 feet**
* `user_scale = 1.50` (Max Frame Width 375mm): **~478 feet**

*(By default, the mathematical constraints guarantee the largest dimension of the entire stand won't exceed `250mm` when scale is `1.0`)*

## 🔧 Assembly Instructions
1. Press the **3 Crossbars** into the hex-sockets of the **Left Stand Frame** and **Right Stand Frame**. Add glue if desired for extra rigidity.
2. Press the **Left Spool Half** and **Right Spool Half** together using the center locking peg.
3. Slide the assembled Spool axle into the main hub bearings of the Stand Frame.
4. Press the **Handle** into the offset hole on the Right Spool flange.
5. Snap/glue the **Locking Caps** onto the ends of the axles protruding through the outside of the Stand Frame to lock the spool in place so it rotates freely without sliding out.
