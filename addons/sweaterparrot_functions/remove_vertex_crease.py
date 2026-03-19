import bpy

class RemoveVertexCrease(bpy.types.Operator):
    """
    Set selected vertices crease to -1, effectively removing it
    """

    bl_idname = "mesh.remove_vertex_crease"
    bl_label = "Remove Vertex Crease"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.ops.transform.vert_crease(value=-1.0)
        return {'FINISHED'}

class RemoveVertexCreaseButton(bpy.types.Operator):
    bl_idname = "object.mesh.remove_vertex_crease"
    bl_label = "Runs 'remove vertex crease'"

    def execute(self, context):
        scene = context.scene

        bpy.ops.transform.vert_crease(value=-1.0)
        return {'FINISHED'}


def draw_menu(self, context):
    layout = self.layout
    layout.operator("mesh.remove_vertex_crease", text="Remove Vertex Crease", icon ='TRASH')

def register():
    bpy.utils.register_class(RemoveVertexCrease)
    bpy.types.VIEW3D_MT_edit_mesh_delete.append(draw_menu)

def unregister():
    bpy.types.VIEW3D_MT_edit_mesh_delete.remove(draw_menu)
    bpy.utils.unregister_class(RemoveVertexCrease)

def draw_panel_ui(layout, context):
    scene = context.scene
    row = layout.row()

    layout.operator(RemoveVertexCreaseButton.bl_idname)