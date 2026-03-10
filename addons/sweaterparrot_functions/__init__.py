import bpy

from . import update_all_emission_colors
from . import toggle_all_lattice_modifiers 
from . import toggle_global_local_keybinding 
from . import mark_sharp_as_seam_and_unwrap 
from . import remove_vertex_crease

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

        toggle_all_lattice_modifiers.draw(layout, context)
        update_all_emission_colors.draw(layout, context)

def register():
    bpy.utils.register_class(SweaterparrotFunctionsPanel)

    toggle_all_lattice_modifiers.register()
    update_all_emission_colors.register()
    toggle_global_local_keybinding.register()
    mark_sharp_as_seam_and_unwrap.register()
    remove_vertex_crease.register()

def unregister():
    toggle_all_lattice_modifiers.unregister()
    update_all_emission_colors.unregister()
    toggle_global_local_keybinding.unregister()
    mark_sharp_as_seam_and_unwrap.unregister()
    remove_vertex_crease.unregister()

    bpy.utils.unregister_class(SweaterparrotFunctionsPanel)

if __name__ == "__main__":
    register()
