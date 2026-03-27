import os
import glob
import subprocess
import sys

def run_part_scripts():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Find all part scripts
    part_files = sorted(glob.glob(os.path.join(script_dir, "part_*.py")))
    
    if not part_files:
        print("No part_*.py files found in the current directory.")
        return
        
    print(f"Found {len(part_files)} part files to execute.")
    print("=" * 40)
    
    success_count = 0
    freecad_cmd = "/Applications/FreeCAD.app/Contents/Resources/bin/freecadcmd"
    
    # Check if freecadcmd exists
    if not os.path.exists(freecad_cmd):
        print(f"Error: Could not find FreeCAD at {freecad_cmd}")
        print("Please ensure FreeCAD is installed.")
        return
    
    for part_file in part_files:
        filename = os.path.basename(part_file)
        print(f"Running {filename}... (this may take a minute or two)")
        
        # We stream output using subprocess.Popen to see progress in real-time
        process = subprocess.Popen(
            [freecad_cmd, part_file],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )
        
        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                # Optionally print output or just key messages
                if "Exporting" in output or "Error" in output:
                    print(f"  > {output.strip()}")
        
        return_code = process.poll()
        
        if return_code == 0:
            print(f"✅ Successfully exported parts from {filename}")
            success_count += 1
        else:
            print(f"❌ Failed to run {filename} (Exit code: {return_code})")
            
        print("-" * 40)
        
    print(f"Finished! Successfully ran {success_count}/{len(part_files)} scripts.")
    print(f"Generated STL and STEP files should be in the exports/ directory.")

if __name__ == "__main__":
    run_part_scripts()
