import bpy


def rename_nodes(*args):
    """
    When duplicating a collection or object hierarchy, blender will rename the collection or root node
    from e.g "Hole_3" to "Hole_3.001", and will give all children this ".001" suffix too
    this function renames "Hole_3.001" to "Hole_4" (or whatever you want the new object to be named)
    This doubles as a general-purpose bulk node renaming function if the suffix parameter isn't supplied
    
    Parameters
    root_name (string):  The copied node name (e.g "Hole_3")
    suffix (string) (optional): The number blender adds to the end when you copy something (e.g "001").
                                If not supplied, this will default to an empty string
    new_name (string): the new name for the node and its children = e.g "Hole_4"
    """

    root_name = ""
    suffix = ""
    new_name = ""

    if len(args) == 2:
        root_name = args[0]
        suffix = ""
        new_name = args[1]
    elif len(args) == 3:
        root_name = args[0]
        suffix = args[1]
        new_name = args[2]
    else:
        raise Exception(f"rename_nodes requires 2 or 3 arguments (got {len(args)})")

    if root_name == "":
        raise Exception("root_name must be supplied")

    if new_name == "":
        raise Exception("new_name must be supplied")
    
    def get_new_name(name):
        if root_name in name and suffix in name:
           return name.replace(root_name, new_name).replace(suffix, "")

        return None

    print("renaming elements with pattern '{root_name}' with '{suffix}' at the end to '{new_name}'")

    obj_count = 0
    for obj in bpy.data.objects:
        new_obj_name = get_new_name(obj.name)

        if new_obj_name is not None:
            obj.name = new_obj_name
            obj_count += 1

    collection_count = 0
    for collection in bpy.data.collections:
        new_collection_name = get_new_name(collection.name)

        if new_collection_name is not None:
            collection.name = new_collection_name
            collection_count += 1

    print(f"Done. Updated {obj_count} object and {collection_count} colleciton names")
    