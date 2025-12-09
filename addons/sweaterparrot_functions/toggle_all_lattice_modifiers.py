import bpy

def set_all_lattice_modifiers_viewport_visibility(should_be_active):
  for obj in bpy.context.view_layer.objects:
    if obj.modifiers:
      for mod in obj.modifiers:
        if mod.type == 'LATTICE':
          mod.show_viewport = should_be_active

class ToggleAllLatticeModifiersOperator(bpy.types.Operator):
    """
    Button that 
    """
    bl_idname = "object.toggle_all_lattice_modifiers"
    bl_label = "Show/hide all lattice objects in scene"

    def execute(self, context):
        global_lattice_show_viewport = context.scene.global_lattice_show_viewport
        set_all_lattice_modifiers_viewport_visibility(global_lattice_show_viewport)

        return {'FINISHED'}

def register():
    bpy.types.Scene.global_lattice_show_viewport = bpy.props.BoolProperty(
        name="Show/hide all lattice objects in scene",
        default=True
    )

    bpy.utils.register_class(ToggleAllLatticeModifiersOperator)

def unregister():
    bpy.utils.unregister_class(ToggleAllLatticeModifiersOperator)

    del bpy.types.Scene.new_global_emission_color
