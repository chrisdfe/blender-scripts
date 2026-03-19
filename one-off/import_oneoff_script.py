import sys
import os
import importlib
from types import SimpleNamespace

MODULES_TO_IMPORT = [
    # Add individual modules here
]

# Change this if neccessary
MODULES_DIR = "Q:/Documents/projects/blender-scripts/one-off/"

def import_from_disk(module_name, module_path):
    abs_path = os.path.abspath(module_path)
    
    if not os.path.exists(abs_path):
        raise FileNotFoundError(f"The directory '{abs_path}' does not exist.")

    if abs_path not in sys.path:
        sys.path.append(abs_path)

    if module_name in sys.modules:
        return importlib.reload(sys.modules[module_name])
    
    return importlib.import_module(module_name)
  
def import_all_from_disk(module_names, module_path):
    result_dict = {} 

    for module_name in module_names:
        imported_module = import_from_disk(module_name, module_path)
        imports = {k: v for k, v in vars(imported_module).items() if not k.startswith('_')}
        result_dict.update(imports)

    result = SimpleNamespace(**result_dict)
    return result

# Import like this:
# tools = import_all_from_disk(MODULES_TO_IMPORT, MODULES_DIR)

# Use like this
# tools.select_all_with_material("Water")
