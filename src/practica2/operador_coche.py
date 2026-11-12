import bpy # type: ignore # Añadiendo ese comentario se ignora el falso warning de VSC
import crear_coche as coche
from importlib import reload

reload(coche) # Recarga el script de crear_coche

# Clase que extiende del tipo operador para generar la ciudad
class GenerateCarOperator(bpy.types.Operator):
    """Genera un coche"""
    bl_idname = "object.gen_car" # ID que se añadirá al bpy.ops.(object.gen_ciudad)
    bl_label = "Car Generator" # Nombre del operador

    def execute(self, context):
        
        scene = context.scene # Variable de la escena
        
        for i in range(scene.ncoches): # Bucle que crea el número de coches deseado
           
            coche.crear_coche(scene) # Llama a la función para crear el coche pasándole la escena para usar sus propiedades
        
        return {"FINISHED"}
        
def register():
    bpy.utils.register_class(GenerateCarOperator) # Registra la clase creada del operador


def unregister():
    bpy.utils.unregister_class(GenerateCarOperator) # Elimina el registro la clase creada del operador


if __name__ == "__main__": # Si el script es ejecutado directamente se llama a la función register.
    register()