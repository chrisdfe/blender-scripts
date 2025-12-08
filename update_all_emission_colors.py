import bpy

TARGET_NODE_NAMES = ["Principled BSDF"]

# Test

def update_all_emission_colors(new_color):
    """
    Updates the emission color of all materials in the project
    that have a Principled BSDF node with the Emission Color set to greater than 0
    """
    new_color_tuple = hex_to_normalized_rgb(new_color)
    
    for mat in bpy.data.materials:
        print(mat.name)
        node = get_emission_node(mat)
        if node is not None:
            print(f'Updating {mat.name} emission color to {new_color}')
            node.inputs["Emission Color"].default_value = new_color_tuple
        else:
            print(f'Not updating emission for {mat.name}')

def get_emission_node(mat):
    """
    Returns the emission color node in a material, if it exists
    and the Emission Strength property is not set to 0
    """    
    for node in mat.node_tree.nodes:
        is_target_node = False
        
        # Search for a substring instead of a match
        # to account for names like "Principled BSDF.001"
        # TODO - using a 'node type' would be safer, if that exists
        for target_node_name in TARGET_NODE_NAMES:
            if target_node_name in node.name:
                is_target_node = True
                break

        if is_target_node:
            if node.inputs["Emission Strength"].default_value > 0:
                return node
            else:
                return None
        
    return None

def hex_to_normalized_rgb(hex):
    """
    Converts a hexadecimal string into rgb(a), with values normalized from 0-1 (not 0-255)
    """
    while hex.startswith("#"):
        hex = hex[1:]
    
    hex_len = len(hex)

    # TODO - support 3/4 length hexes
    if hex_len not in [6, 8]:
        raise Exception(f'Invalid hex length - {hex_len}')
    
    r_str = hex[0] + hex[1]
    g_str = hex[2] + hex[3]
    b_str = hex[4] + hex[5]
    a_str = "ff"

    if hex_len == 8:
        a_str = hex[6] + hex[7]
    
    r_int = int(r_str, 16)
    g_int = int(g_str, 16)
    b_int = int(b_str, 16)    
    a_int = int(a_str, 16)

    r = srgb_to_linear(r_int / 255.0)
    g = srgb_to_linear(g_int / 255.0)
    b = srgb_to_linear(b_int / 255.0)
    a = srgb_to_linear(a_int / 255.0)
    
    return (r, g, b, a)

def srgb_to_linear(c):
    """
    Converts a single sRGB color channel value (0.0 to 1.0) 
    to a linear color channel value (0.0 to 1.0).
    """
    if c < 0:
        return 0
    elif c < 0.04045:
        return c / 12.92
    else:
        return ((c + 0.055) / 1.055) ** 2.4    

update_all_emission_colors("#5C1D2BFF")
