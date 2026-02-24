import bpy

RED_LAYER_PATTERN = "(R)"
GREEN_LAYER_PATTERN = "(G)"
BLUE_LAYER_PATTERN = "(B)"
ALPHA_LAYER_PATTERN = "(A)"

BLACK = (0, 0, 0, 0)

def validate_channel(channel):
  if channel not in ['r', 'g', 'b', 'a']:
    raise Exception(f"channel param must be one of 'r', 'g', 'b', or 'a' (is '{channel}')")

def replace_channel_with_new_color(current_color, new_color, channel):
  result = current_color
  current_color_r, current_color_g, current_color_b, current_color_a = current_color
  new_color_r, new_color_g, new_color_b, new_color_a = new_color

  if channel == 'r':
    result = (
      new_color_r,
      current_color_g,
      current_color_b,
      current_color_a,
    )
  elif channel == 'g':
    result = (
      current_color_r,
      new_color_g,
      current_color_b,
      current_color_a,
    )
  elif channel == 'b':
    result = (
      current_color_r,
      current_color_g,
      new_color_b,
      current_color_a,
    )
  elif channel == 'a':
    result = (
      current_color_r,
      current_color_g,
      current_color_b,
      new_color_a,
    )

  return result

def set_channel_data_to_static_color_on_attribute(dest_attr, color_value, channel):
  validate_channel(channel)  

  print(f"writing the static color ({color_value}) to channel {channel} on {dest_attr}")

  for i in range(len(dest_attr.data)):
    current_color = dest_attr.data[i].color
    new_color = replace_channel_with_new_color(current_color, color_value, channel)
    dest_attr.data[i].color = new_color

# channel == a string, either 'r', 'g', 'b', or 'a'
def copy_channel_data_to_attribute(dest_attr, source_attr, channel):
  if (len(source_attr.data) != len(dest_attr.data)):
    raise Exception(f"attr lengths not equal: {source_attr.name} has a length of {len(source_attr)} and {dest_attr.name} has a length of {len(dest_attr)}")
  
  validate_channel(channel)  

  print(f"Writing {channel} channel to {dest_attr.name} from {source_attr.name}")

  for i in range(len(source_attr.data)):
    new_color = source_attr.data[i].color
    current_color = dest_attr.data[i].color
    
    new_color_on_channel = replace_channel_with_new_color(current_color, new_color, channel)
    dest_attr.data[i].color = new_color_on_channel

def pack_rgb_color_attributes_in_obj(obj):
  mesh = obj.data
  if not mesh.color_attributes:
    print(f"Object {obj.name} has no color attribute layers")
    return

  if len(mesh.color_attributes) == 1:
    print(f"Object {obj.name} has only 1 color attribute layer. skipping")
    return

  vertex_color_layer = None
  red_layer = None
  green_layer = None
  blue_layer = None
  alpha_layer = None

  i = 0
  for color_attribute in mesh.color_attributes:
    if i == 0:
      vertex_color_layer = color_attribute
    elif color_attribute.name.endswith(RED_LAYER_PATTERN):
      red_layer = color_attribute
    elif color_attribute.name.endswith(GREEN_LAYER_PATTERN):
      green_layer = color_attribute
    elif color_attribute.name.endswith(BLUE_LAYER_PATTERN):
      blue_layer = color_attribute
    elif color_attribute.name.endswith(ALPHA_LAYER_PATTERN):
      alpha_layer = color_attribute

    i += 1

  if red_layer is None and green_layer is None and blue_layer is None and alpha_layer is None:
    print(f"No R/G/B/A channel layers found on {obj.name} - nothing to pack. skipping")
    return

  channel_layer_tuples = [
    ('r', red_layer),
    ('g', green_layer),
    ('b', blue_layer),
    ('a', alpha_layer),
  ]

  print(f"Writing to {obj.name}")
  for (channel, layer) in channel_layer_tuples:
    if layer is None:
      set_channel_data_to_static_color_on_attribute(vertex_color_layer, BLACK, channel)
    else:
      copy_channel_data_to_attribute(vertex_color_layer, layer, channel)

def pack_rgb_color_attributes_in_selected():
  for obj in bpy.context.selected_objects:
    if obj.type != 'MESH':
      print(f"Object {obj.name} is not a mesh (is {obj.type}). skipping")
      continue
  
    pack_rgb_color_attributes_in_obj(obj)
    
pack_rgb_color_attributes_in_selected()