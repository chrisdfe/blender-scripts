import bpy

class RemoveVertexCrease(bpy.types.Operator):
    """
    Set selected vertices crease to -1
    """

    bl_idname = "mesh.vertex_crease_minus_one"
    bl_label = "Vertex Crease -1"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.ops.transform.vert_crease(value=-1.0)
        return {'FINISHED'}

def register():
    bpy.utils.register_class(RemoveVertexCrease)

def unregister():
    bpy.utils.unregister_class(RemoveVertexCrease)