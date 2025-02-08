import bpy

def set_active_render_layer_for_all_selected(uv_layer_name):
    """
    Sets the active, 'working' UV layer for all selected objects at once.
    Useful when using multiple UV layers, assigned to multiple objects at once
    As of Blender 4.3 it appears there's no way of doing this easily through the UI
    (although I could be wrong about this)

    Parameters:
    uv_layer_name (string): the name of the uv_layer
    """
    for obj in bpy.context.selected_objects:
        if obj.data != None:
            if hasattr(obj.data, "uv_layers"):
                for uv_layer in obj.data.uv_layers:
                    if uv_layer.name == uv_layer_name:
                        obj.data.uv_layers.active = uv_layer
                        uv_layer.active = True
                        uv_layer.active_render = True
                    else:
                        uv_layer.active = False
                        uv_layer.active_render = False