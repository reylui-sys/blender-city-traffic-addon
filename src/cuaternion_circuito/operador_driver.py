import bpy # type: ignore # Añadiendo ese comentario se ignora el falso warning de VSC
import os
from borrar_elementos import delete
from posicion import asigna_driver_posicion, asigna_driver_cuaternion

# Clase que extiende del tipo operador para generar la ciudad
class GenerateDriverOperator(bpy.types.Operator):
    """Este es un operador crea la trayectoria con la interpolación seleccionada"""
    bl_idname = "object.get_posicion" # ID que se añadirá al bpy.ops.(object.get_posicion)
    bl_label = "Driver Object Generator" # Nombre del operador
    bl_description = "Genera una trayectoria para el objeto seleccionado usando drivers para las coordenadas"

    def execute(self, context):
        obj = context.object # Se guarda el objeto en la variable obj
        scene = context.scene
        nombre_ob = obj.name # Se guarda el nombre del objeto en una variable
        modelo = obj.modelo # Se guarda el modelo en la variable modelo
        
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
        # Comprueba si hay algo escrito en el modelo. De ser así ignora la importación
        if modelo != "":
            # Coge el directorio absoluto y lo añade al relativo creado por blender
            dirname = os.path.dirname(bpy.data.filepath)
            filepath = dirname + modelo # Tuvimos que usar "+" en lugar del join porque daba error 
            
            # Comprueba si el directorio existe
            if os.path.exists(filepath):
                bpy.ops.wm.obj_import(filepath=filepath) # Importa el modelo de dicho directorio
                car = bpy.context.active_object # Asigna a una varible el objeto importado
                
                """
                Me di cuenta de que el error estaba en que se intentaba interpolar un objeto sin los keyframes del objeto anterior (Cubo).
                Por ello decidí crear una función nueva (para no hacer más engorrosa esta parte) y copiar todas las fcurves al coche. La función se puede usar para otras prácticas
                """
                copiarFcurves(obj, car, "location") # Copia las fcurve de location al nuevo objeto
                copiarFcurves(obj, car, "velocidad") # Copia las fcurve de velocidad al nuevo objeto
                
                car.scale = [10,10,10] # Escala el coche para que no sea tan pequeñp
                obj = car # Asigna el coche a la varible que pertenecia al anterior objeto
                
                delete(nombre_ob) # Borra el objeto anterior. (Función de prácticas anteriores)
        
        # Bucle que llama a la funcion de asignar drivers 3 veces (uno por coordenada)
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
      
        # Comprueba si se ha habilitado la rotación
        if obj.rotacion == True:
            # Cambia el modo de rotación
            obj.rotation_mode = 'QUATERNION'
            # Bucle que asigna el driver a cada componente del cuaternión
            for d in range(4):
                asigna_driver_cuaternion(obj, d) # Llama 4 veces a la función asigna driver
            
        return {"FINISHED"}
    
"""
Para hacer esta función se ha usado como referencia una parte del código de la práctica 2 más algo de ayuda del ChatGPT
Por ejemplo la condición "if not obj_destino.animation_data.action:" ha sido realizado por gpt y la parte de nueva_fcurve.keyframe_points.clear() y el fcurve.data_path

"""
def copiarFcurves(obj_fuente, obj_destino, target_fcurve):

    # Crea los datos de animación del objeto destino (Coche)
    obj_destino.animation_data_create()
    
    # Se asigna a una variable el action del objeto fuente (Cubo)
    fuente_action = obj_fuente.animation_data.action
    
    # Si no se ha creado ninguna action para el objeto destino (Coche) se crea bajo el nombre CarAction
    if not obj_destino.animation_data.action:
        obj_destino.animation_data.action = bpy.data.actions.new(name="CarAction")
    
    # Esa nueva action creada se asigna a una variable
    destino_action = obj_destino.animation_data.action
    
    # Bucle que recorre las fcurves de la action del objeto fuente (Cubo)
    for fcurve in fuente_action.fcurves:
        # Comprueba si el data_path (location, velocidad...) coincide con el string pasado como argumentos
        if fcurve.data_path == target_fcurve:
            
            # Crea una nueva fcurve en la action del objeto destino (Coche)
            nueva_fcurve = destino_action.fcurves.new(data_path=fcurve.data_path, index=fcurve.array_index)
            
            # Elimina todos los keyframes de la fcurve creada
            nueva_fcurve.keyframe_points.clear()
            # Bucle que recorre los keyframes de la fcurve actua y se los asigna a la nueva fcurve del objeto destino (Coche)
            for keyframe in fcurve.keyframe_points:
                nueva_fcurve.keyframe_points.insert(keyframe.co[0], keyframe.co[1])
    
def register():
    bpy.utils.register_class(GenerateDriverOperator) # Registra la clase creada del operador

def unregister():
    bpy.utils.unregister_class(GenerateDriverOperator) # Elimina el registro la clase creada del operador

if __name__ == "__main__": # Si el script es ejecutado directamente se llama a la función register.
    register()