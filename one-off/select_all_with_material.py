import bpy

def obj_has_matching_material(obj, material_name):
  for slot in obj.material_slots:
    if slot.material and slot.material.name == material_name:
      return True

  return False

def select_all_with_material(material_name, print_name=False):
  bpy.ops.object.select_all(action='DESELECT')

  count = 0
  for obj in bpy.context.scene.objects:
    for slot in obj.material_slots:
      if slot.material and slot.material.name == material_name:
        if obj_has_matching_material(obj, material_name):
          obj.select_set(True)

          count += 1

          if (print_name):
            print(f"{obj.name}")

  print(f"Done. Selected {count} objects with material '{material_name}'")
