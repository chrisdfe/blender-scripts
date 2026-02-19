import bpy

def replace_uv_maps(new_layer_names):
    obj = bpy.context.active_object
    
    if obj is None:
        raise Exception("No active object selected")
        
    if obj.type != 'MESH':
        raise Exception("Object must be a mesh")
        
    # Remove existing layers first
    mesh = obj.data
    while mesh.uv_layers:
        mesh.uv_layers.remove(mesh.uv_layers[0])
    
    # Add new layers
    for new_layer_name in new_layer_names:
        # Create layer
        layer = mesh.uv_layers.new(name=new_layer_name)
        layer.active = True
        layer.active_render = True

        # Auto-unwrap
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='SELECT')

        bpy.ops.uv.smart_project(angle_limit=66.0, island_margin=0.0)

        bpy.ops.object.mode_set(mode='OBJECT')