import bpy #type: ignore
from .borrar_elementos import delete

class DeleteCity(bpy.types.Operator):
    """Elimina todos los coches"""
    bl_idname = "object.delete_cars" # ID que se añadirá al bpy.ops.(object.gen_ciudad)
    bl_label = "Car Eraser" # Nombre del operador

    def execute(self, context):
        delete("Coche")
        return {'FINISHED'}

# Register and add to the "object" menu (required to also use F3 search "Simple Object Operator" for quick access).
def register():
    bpy.utils.register_class(DeleteCity)

def unregister():
    bpy.utils.unregister_class(DeleteCity)

if __name__ == "__main__":
    register()