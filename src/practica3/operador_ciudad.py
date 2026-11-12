import bpy # type: ignore # Añadiendo ese comentario se ignora el falso warning de VSC
from city_gen import create_city as crear
from borrar_elementos import delete as borrar

# Clase que extiende del tipo operador para generar la ciudad
class GenerateCityOperator(bpy.types.Operator):
    """Genera la ciudad"""   
    bl_idname = "object.gen_ciudad" # ID que se añadirá al bpy.ops.(object.gen_ciudad)
    bl_label = "City Generator" # Nombre del operador

    def invoke(self, context, event):
        scene = context.scene # Se instancia guarda el contexto de la escena en una variable
        
        nx = scene.n_calles_x # Numero de calles en el eje X
        ny = scene.n_calles_y # Numero de calles en el eje Y
        
        p = [0, 0] # Se añaden las coordenadas en un vector

        # Anchura de los edificios (l), anchura de las calles (w) y altura de los edificios (h)
        l = scene.tam_manzana
        w = scene.ancho_calles
        
        # Rango de valores para generar la altura aleatoria
        min_h = scene.alt_edif_min
        max_h = scene.alt_edif_max
        
        # Funcion que elimina los edificios, las "manzanas" ya existentes
        borrar("Manzana")
        
        # Llamada a la funcion para crear la ciudad
        crear(p, nx, ny, l, w, min_h, max_h)
        
        return {"FINISHED"}
        
def register():
    bpy.utils.register_class(GenerateCityOperator) # Registra la clase creada del operador


def unregister():
    bpy.utils.unregister_class(GenerateCityOperator) # Elimina el registro la clase creada del operador


if __name__ == "__main__": # Si el script es ejecutado directamente se llama a la función register.
    register()