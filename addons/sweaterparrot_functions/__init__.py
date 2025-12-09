import bpy
from .update_all_emission_colors import (
  register as register_update_all_emission_colors,
  unregister as unregister_update_all_emission_colors,
  UpdateGlobalEmissionColorOperator
)

from .toggle_all_lattice_modifiers import (
    register as register_toggle_all_lattice_modifiers,
    unregister as unregister_toggle_all_lattice_modifiers,
    ToggleAllLatticeModifiersOperator
)

bl_info = {
    "name": "Sweaterparrot Functions",
    "author": "Christopher Ferris",
    "version": (1, 0),
    "blender": (4, 3, 0),
    "location": "3D View > Sidebar > Scene Tab",
    "description": "A sidebar panel for functions I commonly use in Blender.",
    "category": "Development",
}

class SweaterparrotFunctionsPanel(bpy.types.Panel):
    """
    Creates a panel for functions I commonly use
    """
    bl_label = "Sweaterparrot Functions"
    bl_idname = "SweaterparrotFunctionsPanel"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_category = "Scene"
    bl_context = "render"

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        row = layout.row()

        # TODO - split this into draw methods in each file
        # Update global emission color
        layout.label(text="Update global emission color", icon='WORLD_DATA')
        layout.prop(scene, "new_global_emission_color", text="New global emission color")
        layout.operator(UpdateGlobalEmissionColorOperator.bl_idname)

        # Toggle all lattice modifiers
        layout.label(text="Toggle all lattice modifiers", icon='LATTICE_DATA')
        layout.prop(scene, "global_lattice_show_viewport", text="Show/hide all lattice objects in scene")
        layout.operator(ToggleAllLatticeModifiersOperator.bl_idname)


def register():
    bpy.utils.register_class(SweaterparrotFunctionsPanel)

    register_update_all_emission_colors()
    register_toggle_all_lattice_modifiers()

def unregister():
    unregister_toggle_all_lattice_modifiers
    unregister_update_all_emission_colors()

    bpy.utils.unregister_class(SweaterparrotFunctionsPanel)

if __name__ == "__main__":
    register()
