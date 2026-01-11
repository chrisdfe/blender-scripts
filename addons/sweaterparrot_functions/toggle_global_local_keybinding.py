import bpy

class ViewportOrientationToggler(bpy.types.Operator):
    """
    Toggles between Global and Local transform orientations
    """
    bl_idname = "view3d.toggle_global_local"
    bl_label = "Toggle Global/Local Orientation"

    def execute(self, context):
        slots = context.scene.transform_orientation_slots

        if slots.type == 'GLOBAL':
            slots.type = 'LOCAL'
        else:
            slots.type = 'GLOBAL'
        
        self.report({'INFO'}, f"New orientation: {slots.type}")

        return {'FINISHED'}

addon_keymaps = []

def register():
    bpy.utils.register_class(ViewportOrientationToggler)
    
    # Add keymap entry
    window_manager = bpy.context.window_manager
    key_configs = window_manager.keyconfigs.addon
    if key_configs:
        keymaps = key_configs.keymaps.new(name='3D View', space_type='VIEW_3D')
        keymap_item = keymaps.keymap_items.new(ViewportOrientationToggler.bl_idname, 'T', 'PRESS', ctrl=True, shift=True)
        addon_keymaps.append((keymaps, keymap_item))

def unregister():
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)

    addon_keymaps.clear()

    bpy.utils.unregister_class(ViewportOrientationToggler)
