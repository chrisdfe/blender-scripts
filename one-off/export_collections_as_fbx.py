import time
import bpy
import os
from functools import partial

PRESET_NAME = "Unity"

class PresetContainer:
    def __init__(self):
        self.settings = {}

    def __setattr__(self, name, value):
        if name == 'settings':
            super().__setattr__(name, value)
        else:
            self.settings[name] = value

def get_preset_settings(preset_name):
    """
    Finds and returns settings from a saved FBX export preset.
    """
    preset_subdir = 'operator/export_scene.fbx'
    filepath = bpy.utils.preset_find(preset_name, preset_subdir)

    if not filepath:
        raise Exception(f"Preset '{preset_name}' not found.")

    op = PresetContainer()

    # Execute the preset file. Presets expect an 'op' object to exist in the namespace.
    with open(filepath, 'r') as f:
        lines = f.readlines()
        
        # Filter out lines that try to redefine 'op' 
        # (e.g., 'op = bpy.context.active_operator')
        cleaned_preset = ""
        for line in lines:
            # We already have our own imported bpy
            if line.strip().startswith("import bpy"):
                continue
            # We want to keep our 'op_mock' as the 'op' variable
            if line.strip().startswith("op ="):
                continue

            cleaned_preset += line

        exec(cleaned_preset, {"op": op, "bpy": bpy})

    # Manually set this here, because this is required for this whole script to work
    op.settings['use_selection'] = True
    return op.settings


def get_collections_by_name_list(collection_name_list):
    result = []

    for name in collection_name_list:
        # Doing it this way around instead of iterating through collections + building a list
        # so we can fail explicitly if a collection wasn't found
        collection = bpy.data.collections[name]

        if collection is None:
            raise Exception(f"collection with name '{name}' not found!")
        
        result.append(collection)

    return result

def select_all_objects_in_collection(collection):
    bpy.ops.object.select_all(action='DESELECT')
    bpy.context.view_layer.update()

    has_set_active = False
    for obj in collection.all_objects:
        obj.select_set(True)

        # For whatever reason this whole script fails unless there's an "active object", so we ensure that here
        if not has_set_active:
            bpy.context.view_layer.objects.active = obj
            has_set_active = True

            # 
            bpy.context.view_layer.update()

    bpy.context.view_layer.update()
   
WAIT_FOR_UNHIDE_INTERVAL = 0.1
WAIT_FOR_SELECTION_INTERVAL = 0.1
WAIT_TO_EXPORT_NEXT_COLLECTION_INTERVAL = 2

def export_collection_as_fbx(collection, settings, base_export_path, name_prefix):

    print(f"exporting {collection.name}...")
    print(f"selecting {len(collection.all_objects)} items in {collection.name}")
    select_all_objects_in_collection(collection)

    def after_select():
        selected_count = len(bpy.context.selected_objects)
        print(f"exporting {selected_count} items in {collection.name}")
      
        # e.g HotSprings_9_Entrance.fbx
        filename = f"{name_prefix}_{collection.name}.fbx"
        export_path = os.path.join(base_export_path, filename)
        settings["filepath"] = export_path
        settings["use_selection"] = True
        settings["use_visible"] = True

        bpy.ops.export_scene.fbx(**settings)

        print(f"Exported collection {selected_count}/{len(collection.all_objects)} objects in '{collection.name}' as {export_path}")
        print("\n")
    
    # wait for the selection to actually occur
    bpy.app.timers.register(after_select, first_interval=WAIT_FOR_SELECTION_INTERVAL)

# def get_whitelisted_parent(obj, allowed_collection_names):
#     pass

# def export_active_object_collection_as_fbx(allowed_collection_names, subfolder, name_prefix):
#     base_export_path = bpy.path.abspath(bpy.path.abspath("//") + f"/{subfolder}") 
#     settings = get_preset_settings(PRESET_NAME)

#     active_obj = bpy.context.active_object
#     top_level_parent = get_whitelisted_parent(obj, allowed_collection_names)

#     print(f"{active_obj} is in ")

def export_collections_as_fbx(collection_names, subfolder, name_prefix):
    """
    collection_names (string[])
    subfolder (string): relative to the blender file being exported from
    name_prefix (string)
    """

    base_export_path = bpy.path.abspath(bpy.path.abspath("//") + f"/{subfolder}") 

    settings = get_preset_settings(PRESET_NAME)

    collections = get_collections_by_name_list(collection_names)

    print("unhiding items in collections...") 

    # Unhide everythign so it's selectable
    objects_to_rehide = []
    for collection in collections:
        for obj in collection.all_objects:
            if (obj.hide_get()):
                objects_to_rehide.append(obj)
                obj.hide_set(False)


    print(f"{len(objects_to_rehide)} object{'' if len(objects_to_rehide) == 0 else 's'} unhidden");

    def rehide_all():
        print(f"rehiding {len(objects_to_rehide)} item{'' if len(objects_to_rehide) == 1 else 's'} in collections...")
        for obj in objects_to_rehide:
            obj.hide_set(True)

    def continue_exporting():
        print(f"Exporting {len(collections)} collection{'' if len(collections)}...")

        idx = 1
        for collection in collections:
            # 
            interval = idx * WAIT_TO_EXPORT_NEXT_COLLECTION_INTERVAL
            export_this_collection = partial(export_collection_as_fbx, collection, settings, base_export_path, name_prefix)
            bpy.app.timers.register(export_this_collection, first_interval=interval)

            idx += 1
        
        def print_done():
            print("Done.")
        
        interval = idx * WAIT_TO_EXPORT_NEXT_COLLECTION_INTERVAL
        bpy.app.timers.register(rehide_all, first_interval=interval)

        interval += WAIT_FOR_UNHIDE_INTERVAL
        bpy.app.timers.register(print_done, first_interval=interval)
        
    bpy.app.timers.register(continue_exporting, first_interval=WAIT_FOR_UNHIDE_INTERVAL)
        
def get_parent_ancestry(obj):
    """
    Traverses up the tree, from object up to root root
    Returns a list of collection names in object -> root order
    """
    current_collection = obj.users_collection[0]
    result = [current_collection]
    
    keep_going = True
    while keep_going:
        has_found_parent = False
        for collection in bpy.data.collections:
            if current_collection.name in collection.children:
                current_collection = collection
                result.append(current_collection)
                has_found_parent = True
                break

        # We're at the root if this is the case - we are now done
        if has_found_parent == False:
            keep_going = False
        
    return result

def export_active_object_collections(collection_names, subfolder, name_prefix):
    obj = bpy.context.active_object
    # current_collection = obj.users_colletion
    parent_collections = get_parent_ancestry(obj)
    
    parent_collections_to_export = []
    for parent in parent_collections:
        if parent.name in collection_names:
            parent_collections_to_export.append(parent.name)
    
    export_collections_as_fbx(parent_collections_to_export, subfolder, name_prefix)