import bpy

from .update_all_emission_colors import UPDATE_ALL_EMISSION_COLORS
from .toggle_all_lattice_modifiers import TOGGLE_ALL_LATTICE_MODIFIERS

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

        TOGGLE_ALL_LATTICE_MODIFIERS.draw(layout, context)
        UPDATE_ALL_EMISSION_COLORS.draw(layout, context)

def register():
    bpy.utils.register_class(SweaterparrotFunctionsPanel)

    TOGGLE_ALL_LATTICE_MODIFIERS.register()
    UPDATE_ALL_EMISSION_COLORS.register()


def unregister():
    TOGGLE_ALL_LATTICE_MODIFIERS.unregister()
    UPDATE_ALL_EMISSION_COLORS.unregister()

    bpy.utils.unregister_class(SweaterparrotFunctionsPanel)

if __name__ == "__main__":
    register()
