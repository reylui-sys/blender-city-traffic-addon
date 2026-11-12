import bpy # type: ignore # Añadiendo ese comentario se ignora el falso warning de VSC
from posicion import asigna_driver_posicion

# Clase que extiende del tipo operador para generar la ciudad
class GenerateDriverOperator(bpy.types.Operator):
    """Este es un operador crea la trayectoria con la interpolación seleccionada"""
    bl_idname = "object.get_posicion" # ID que se añadirá al bpy.ops.(object.get_posicion)
    bl_label = "Driver Object Generator" # Nombre del operador
    bl_description = "Genera una trayectoria para el objeto seleccionado usando drivers para las coordenadas"

    def execute(self, context):
        obj = context.object # Se guarda el objeto en la variable obj
        scene = context.scene # Se guarda la escena en la variable escene
        
        # Se pasan todas los valores de la escena (el panel) al objeto
        # para realizar el calculo sobre él
        obj.tension = scene.scene_tension
        obj.velocidad = scene.scene_velocidad # Creo que se puede omitir
        obj.metodo = scene.scene_metodo

        """
        Aquí lo que se pretende es copiar toda la curva de la velocidad de la escena a la curva creada para el objeto.
        De esta forma en Hermite se podrá realizar la interpolación sin pasarle la escena
        
        Tanto el objeto como la escena tienen unos datos de animación "animation_data" y se crean por código así:
        
        obj = bpy.context.active_object (por ejemplo)
        obj.animation_data_create()
        
        Después se crea una acción que contendrá las fcurves: obj.animation_data.action = bpy.data.actions.new(name="NombreAccion")
        
        Y finalmente la fcurve dentro de la action: obj.animation_data.action.fcurve.new(data_path="propiedad_X", index=n, action_group="NombreAccion")
        
        En el data_path se pone la propiedad a la que se quiera añadir keyframes, ya sea location, rotation_euler, velocidad (creada anteriormente)...
        El action_group especifíca donde queremos que agrupe la curva. En el graph editor se puede ver perfectamente la agrupación si se usa. Por ejemplo
        dentro de las fcurves del objeto se puede tener el action_group que agrupe location y scale y otro las propiedades creadas por nosotros. Así en el
        graph editor en vez de tenerlas seguidas en el objeto estarán como en "pestañas" diferentes
        
        Se pasa de esto:
        
        >objectAction.001
                - x location
                - y location 
                - z location 
                - [0]velocidad
                - [1]velocidad
                - [2]velocidad
                
        a esto:
        
        >objectAction.001
                >BlenderGroup
                    - x location
                    - y location 
                    - z location 
                >CityGroup
                    - [0]velocidad 
                    - [1]velocidad
                    - [2]velocidad
        
        """
        for i in range(3):
            
            # Se guardan las curvas de la velocidad de la escena y el objeto para las 3 coordenadas
            fcurve_scene = scene.animation_data.action.fcurves.find("scene_velocidad", index=i)
            fcurve_obj = obj.animation_data.action.fcurves.find("velocidad", index=i)
            
            # Se itera sobre todos los keyframes de la curva de la escena
            for k in range(len(fcurve_scene.keyframe_points)):
                
                # Se obtiene el valor del frame del keyframe iterado
                frame_actual = fcurve_scene.keyframe_points[k].co[0]
                
                # Se inserta un nuevo keyframe para la curva del objeto "encima" del de la escena 
                obj.keyframe_insert(data_path="velocidad", frame=frame_actual)
            
                # Se asigna el valor del keyframe de las dos curvas, se "copia" el keyframe
                fcurve_obj.keyframe_points[k].co[1] = fcurve_scene.keyframe_points[k].co[1]

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