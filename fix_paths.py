import glob, os, re

files = glob.glob('part_*.py') + ['assembly.py']

for fname in files:
    with open(fname, 'r') as f:
        content = f.read()

    robust_header = """import sys, os
try:
    _script_dir = os.path.dirname(os.path.abspath(__file__))
except NameError:
    _script_dir = os.getcwd()
if _script_dir not in sys.path:
    sys.path.insert(0, _script_dir)
"""

    # Fix the top imports
    content = content.replace("import sys, os\nsys.path.append(os.path.dirname(os.path.abspath(__file__)))\n", robust_header)
    
    # Fix the exports dir in the __main__ block
    content = content.replace("export_dir = os.path.join(os.path.dirname(__file__), 'exports')", "export_dir = os.path.join(_script_dir, 'exports')")
    content = content.replace('export_dir = os.path.join(os.path.dirname(__file__), "exports")', 'export_dir = os.path.join(_script_dir, "exports")')

    with open(fname, 'w') as f:
        f.write(content)

print("Finished fixing freecad paths.")
