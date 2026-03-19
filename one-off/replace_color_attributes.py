import bpy
import os
import sys
import importlib

def import_one_off_module(module_name):
  text_block = bpy.context.space_data.text
  if not (text_block and text_block.filepath):
    raise RuntimeError(f"Cannot reload relative module - active text editor block is not saved to disk")

  script_dir = os.path.dirname(os.path.abspath(text_block.filepath))
  
  if script_dir not in sys.path:
      sys.path.append(script_dir)
  
  if module_name in sys.modules:
    return importlib.reload(sys.modules[module_name])
  
  return importlib.import_module(module_name) 

pack_rgba_color_attributes = import_one_off_module("pack_rgba_color_attributes")

def replace_color_attributes(obj, new_channel_configs):
  if not obj or obj.type != 'MESH':
      print(f"{obj.name} must be a mesh (is a {obj.type}) - skipping")
      return
    
  print(f"Replacing color attribtues of {obj.name}")

  # Clear out existing color attributes first
  while obj.data.color_attributes:
    obj.data.color_attributes.remove(obj.data.color_attributes[0])
  
  # Create new channels
  for (new_channel_name, new_channel_default_color) in new_channel_configs:
    attr = obj.data.color_attributes.new(
      name=new_channel_name,
      type="FLOAT_COLOR",
      domain='POINT'
    )

    for data in attr.data:
       data.color = new_channel_default_color
    
  print("Done.")
  
def replace_color_attributes_in_selected(new_channel_configs):
  if bpy.context.mode != 'OBJECT':
    raise RuntimeError("User must be in Object Mode to run this script.")

  for obj in bpy.context.selected_objects:
    replace_color_attributes(obj, new_channel_configs)

# replace_color_attributes_in_selected(WATER_REFLECTION_SURFACE_COLOR_ATTRIBUTES)

def replace_color_attributes_in_selected_and_pack(new_channel_configs):
  if bpy.context.mode != 'OBJECT':
    raise RuntimeError("User must be in Object Mode to run this script.")

  for obj in bpy.context.selected_objects:
    replace_color_attributes(obj, new_channel_configs)
    pack_rgba_color_attributes.pack_rgb_color_attributes_in_obj(obj)
