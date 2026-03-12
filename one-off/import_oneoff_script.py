# 
# Copy & paste all of this to the top of the file to be able to import one-off functions
# 
import sys
import os
import importlib

# Make sure this is the right directory obviously
SWEATERPARROT_FUNCTIONS_ONE_OFF_DIR = "Q:/Documents/projets/blender-scripts/one-off/"

def import_from_disk(module_name, module_path):
    abs_path = os.path.abspath(module_path)
    
    if not os.path.exists(abs_path):
        raise FileNotFoundError(f"The directory '{abs_path}' does not exist.")

    if abs_path not in sys.path:
        sys.path.append(abs_path)

    if module_name in sys.modules:
        return importlib.reload(sys.modules[module_name])
    
    return importlib.import_module(module_name)
  
import_from_disk(SWEATERPARROT_FUNCTIONS_ONE_OFF_DIR)

# Use imported modules here
# e.g
# replace_color_attributes = import_from_disk("replace_color_attributes", SWEATERPARROT_FUNCTIONS_ONE_OFF_DIR)