import bpy

def replace_material(old_name, new_name):
    if old_name not in bpy.data.materials:
        raise RuntimeError(f"Material {old_name} not found in scene")
    
    if new_name not in bpy.data.materials:
        raise RuntimeError(f"Material {new_name} not found in scene")    
    
    old_mat = bpy.data.materials[old_name]
    new_mat = bpy.data.materials[new_name]

    count = 0
    
    for obj in bpy.data.objects:
        if obj.type == 'MESH':
            for slot in obj.material_slots:
                if slot.material == old_mat:
                    slot.material = new_mat
                    print(f"Replaced material on: {obj.name}")
                    count += 1
    
    print(f"Updated {count} materials")
                