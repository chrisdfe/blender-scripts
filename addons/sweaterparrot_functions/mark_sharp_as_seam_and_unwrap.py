import bpy
import bmesh

class SeamsFromSharp(bpy.types.Operator):
  """
  Marks all selected sharp edges as seam 
  """
  bl_idname = "mesh.mark_sharp_as_seams"
  bl_label = "Mark Sharp Edges as Seams"
  bl_options = {'REGISTER', 'UNDO'}

  @classmethod
  def poll(cls, context):
    # Only enable when editing a mesh
    return context.mode == 'EDIT_MESH'

  def execute(self, context):
    mesh = context.edit_object.data
    bm = bmesh.from_edit_mesh(mesh)

    # CRITICAL: Update the selection indices so the script "sees" your selection
    bm.edges.ensure_lookup_table()

    # In Blender 4.x/5.0, this is the standard way to check sharpness in BMesh
    # sharp_layer = bm.edges.layers.bool.get("sharp_edge")

    # if sharp_layer is None:
    #     self.report({'WARNING'}, "No sharp edges found in the mesh data.")
    #     return {'CANCELLED'} 

      # Set sharp edges as seam edges also
    count = 0
    for edge in bm.edges:
        # if edge.select and edge[sharp_layer]:
        if edge.select and not edge.smooth:
            edge.seam = True
            count += 1
        
    bmesh.update_edit_mesh(mesh)
              
    self.report({'INFO'}, f"Marked {count} sharp edges as seams in selected object.")
    return {'FINISHED'}

def add_to_edge_menu(self, context):
    self.layout.separator()
    self.layout.operator(SeamsFromSharp.bl_idname, icon='UV_EDGESEL')

def register():
    bpy.utils.register_class(SeamsFromSharp)
    # VIEW3D_MT_edit_mesh_edges is the ID for the Ctrl + E menu
    bpy.types.VIEW3D_MT_edit_mesh_edges.append(add_to_edge_menu)

def unregister():
    bpy.utils.unregister_class(SeamsFromSharp)
    bpy.types.VIEW3D_MT_edit_mesh_edges.remove(add_to_edge_menu)
