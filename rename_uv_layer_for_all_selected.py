import bpy

def rename_uv_layer_for_all_selected(current_name, new_name):
    """
    Renames all UV Layers with the name current_name to new_name
    Especially helpful when working with multiple UV layers across multiple objects

    Parameters:
    current_name (string): the current name of the UV layer to rename
    new_name (string): the new name of the UV layer
    """
    for obj in bpy.context.selected_objects:
        if obj.data != None:
            if hasattr(obj.data, "uv_layers"):
                for uv_layer in obj.data.uv_layers:
                    if uv_layer.name == current_name:
                        uv_layer.name = new_name