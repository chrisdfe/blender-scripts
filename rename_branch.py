import bpy

def rename_copied_branch(root_name, suffix, new_name):
    """
    When copying an object hierarchy, blender will rename the root node
    from e.g "Hole_3" to "Hole_3.001", and will give all children this ".001" suffix too
    this function renames "Hole_3.001" to "Hole_4" (or whatever you want the new object to be named)
    
    Parameters
    root_name (string):  the copied node name (e.g "Hole_3")
    suffix (string): the number blender adds to the end when you copy something (e.g "001")
    new_name (string): the new name for the node and its children = e.g "Hole_4"
    """

    print("renaming")
    
    try:
        key = root_name + suffix
        node = bpy.data.objects[key]
    except:
        print("no node with name '" + root_name + "' found")
        return
    
    def rename(node):
        node.name = node.name.replace(root_name, new_name).replace(suffix, "")
    
    rename(node)
    
    for child in node.children_recursive:
        rename(child)