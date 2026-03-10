import bpy
import os

PRESET_NAME = "Unity"
EXPORT_DIR = bpy.path.abspath("//")

def get_preset_settings(preset_name):
    """
    Finds and returns settings from a saved FBX export preset.
    """

    filename = preset_name.replace(" ", "_").lower() + ".py"
    preset_paths = bpy.utils.preset_paths('operator/export_scene.fbx/')
    
    for path in preset_paths:
        filepath = os.path.join(path, filename)

        if os.path.exists(filepath):
            # Create a dummy class to store preset variables
            class PresetContainer: pass
            op = PresetContainer()
            
            # Execute the preset file to fill the 'op' object with settings
            with open(filepath, 'r') as f:
                # Presets start with 'import bpy' and a few setup lines; we skip those
                exec(f.read(), globals(), { 'op': op })
            return op.__dict__

    return None

def export_collections_as_fbx(export_path, name_prefix, top_level_only = True):
  export_path = bpy.path.abspath(export_path) 

  settings = get_preset_settings(PRESET_NAME)

  if not settings:
      raise Exception(f"Error: FBX Preset '{PRESET_NAME}' was not found")

  settings['use_selection'] = True

  collections = []
  if top_level_only:
      collections = bpy.context.scene.collection.children
  else:
      collections = bpy.data.collections

  for collection in collections:
      bpy.ops.object.select_all(action='DESELECT')
      
      for obj in collection.objects:
          obj.select_set(True)
      
      filename = f"{name_prefix}_{collection.name}.fbx"
      full_path = os.path.join(export_path, filename)

      if not collection.objects:
        print(f"No objects in collection '{collection.name}'")
        continue

      settings['filepath'] = full_path
      bpy.ops.export_scene.fbx(**settings)
      print(f"Exported collection '{collection.name}' as {full_path} with preset '{PRESET_NAME}'")

