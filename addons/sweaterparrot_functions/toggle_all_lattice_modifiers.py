import bpy

def set_all_lattice_modifiers_viewport_visibility(should_be_active):
  for obj in bpy.context.view_layer.objects:
    if obj.modifiers:
      for mod in obj.modifiers:
        if mod.type == 'LATTICE':
          mod.show_viewport = should_be_active

def execute(self, context):
    global_lattice_show_viewport = context.scene.global_lattice_show_viewport
    set_all_lattice_modifiers_viewport_visibility(global_lattice_show_viewport)

    return {'FINISHED'}

class ToggleAllLatticeModifiers:
  def register(self):
      bpy.types.Scene.global_lattice_show_viewport = bpy.props.BoolProperty(
          name="Show/hide all lattice objects in scene",
          default=True,
          update=execute
      )

  def unregister(self):
      del bpy.types.Scene.global_lattice_show_viewport

  def draw(self, layout, context):
      scene = context.scene

      row = layout.row()

      layout.prop(scene, "global_lattice_show_viewport", text="Show/hide all lattice objects in viewport")

TOGGLE_ALL_LATTICE_MODIFIERS = ToggleAllLatticeModifiers()