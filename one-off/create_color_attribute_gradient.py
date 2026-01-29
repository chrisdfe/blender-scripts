import bpy
import bmesh
import bl_math
from mathutils import Color

from collections import deque

def set_vertex_colors(vertices, color_attribute, color):
  """
  vertices (list of Vertex)
  color_attribute (ColorAttribute)
  color (Color)
  """
  for vertex in vertices:
    # vertex colors don't support alpha (I think) but blender seems to complain if we don't pass one in
    color_attribute.data[vertex].color = (color.r, color.g, color.b, 1.0)
  
def build_color_list(from_color, to_color, distance):
  colors = []

  for d in range(0, distance + 1):
    normalized_progress = d / distance

    r = bl_math.lerp(from_color[0], to_color[0], normalized_progress)
    g = bl_math.lerp(from_color[1], to_color[1], normalized_progress)
    b = bl_math.lerp(from_color[2], to_color[2], normalized_progress)

    color = Color((r, g, b))
    colors.append(color)

  return colors

def get_neighbor_vertices(vertex_indices, visited_indices, bm):
  neighbor_indices = []

  for v_idx in vertex_indices:
    vertex = bm.verts[v_idx]

    for edge in vertex.link_edges:
      other_vertex = edge.other_vert(vertex)

      if other_vertex.index not in visited_indices:
        neighbor_indices.append(other_vertex.index)
        visited_indices.add(other_vertex.index)

  return neighbor_indices

def build_vertex_index_groups(starting_vertices, distance, visited_indices, bm):
  neighbor_list = []
  
  current_indices = starting_vertices
  for current_distance in range(0, distance + 1):
    # For the first iteration we want to use the starting_vertices
    if current_distance > 0:
      current_indices = get_neighbor_vertices(current_indices, visited_indices, bm)

    neighbor_list.append(current_indices)

  return neighbor_list

def create_color_attribute_gradient(from_color, to_color, distance, color_attibute_name):
  """
  Creates a color attribute (aka vertex colors) gradient,
  starting with the current selection of vertices and ending <distance> away from them in every direction

  Parameters:
    attr_name (string):
      The name of the color_attribute to draw to. Raises an exception if this doesn't reference an existing Color Attribute
    from_color (3-tuple (r, g, b)):
      The color to lerp from
    to_color (3-tuple (r, g, b))
      The color to lerp to
    distance (int)
      The total distance (in vertices) to spread the gradient out over. Inclusive 
  """

  obj = bpy.context.edit_object;

  if not obj or obj.type != 'MESH':
    raise RuntimeError("Must be in edit mode and have a mesh selected to run this script")

  obj = bpy.context.active_object
  mesh = obj.data

  if color_attibute_name not in mesh.color_attributes:
    raise RuntimeError(f"{color_attibute_name} color attribute doesn't exist")

  colors = build_color_list(from_color, to_color, distance)

  bm = bmesh.from_edit_mesh(mesh)

  visited_indices = set()

  # Start with current selection
  starting_indices = [v.index for v in bm.verts if v.select]

  for v_idx in starting_indices:
    visited_indices.add(v_idx)

  vertex_index_groups = build_vertex_index_groups(starting_indices, distance, visited_indices, bm)

  bpy.ops.object.mode_set(mode='OBJECT')

  # Note - this must be done in object mode! If I assign this variable while still in edit mode,
  #        color_attribute.data will have a length of 0
  color_attribute = mesh.color_attributes[color_attibute_name]

  for current_distance in range(0, distance + 1):
    current_indices = vertex_index_groups[current_distance]

    # If we have no vertices to color the future iterations also won't, so we just exit early here
    if len(current_indices) == 0:
      break

    color = colors[current_distance]

    set_vertex_colors(current_indices, color_attribute, color)
    
  mesh.update() 
  bpy.ops.object.mode_set(mode='EDIT')

# create_color_attribute_gradient((1.0, 1.0, 1.0), (0.0, 0.0, 0.0), 3, "NoiseIntensity")