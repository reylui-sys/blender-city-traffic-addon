import bpy # type: ignore # Añadiendo ese comentario se ignora el falso warning de VSC
from posicion import asigna_driver_posicion

# Clase que extiende del tipo operador para generar la ciudad
class GenerateDriverOperator(bpy.types.Operator):
    """Este es un operador crea la trayectoria con la interpolación seleccionada"""
    bl_idname = "object.get_posicion" # ID que se añadirá al bpy.ops.(object.get_posicion)
    bl_label = "Driver Object Generator" # Nombre del operador

    def invoke(self, context, event):
        obj = context.object # Se guarda el objeto en la variable obj
        # Bucle que llama a la funcion de asignar drivers 3 veces (uno por coordenada)
        for c in range(3):
            asigna_driver_posicion(obj, c) # Llama 3 veces a la función asigna driver
        return {"FINISHED"}
        
def register():
    bpy.utils.register_class(GenerateDriverOperator) # Registra la clase creada del operador

def unregister():
    bpy.utils.unregister_class(GenerateDriverOperator) # Elimina el registro la clase creada del operador

if __name__ == "__main__": # Si el script es ejecutado directamente se llama a la función register.
    register()