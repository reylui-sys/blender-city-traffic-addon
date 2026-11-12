import bpy # type: ignore # Añadiendo ese comentario se ignora el falso warning de VSC
import os
from mathutils import Vector # type: ignore
from borrar_elementos import delete
from posicion import asigna_driver_posicion, asigna_driver_cuaternion, get_posicion

# Clase que extiende del tipo operador para generar la ciudad
class GenerateDriverOperator(bpy.types.Operator):
    """Este es un operador crea la trayectoria con la interpolación seleccionada"""
    bl_idname = "object.get_posicion" # ID que se añadirá al bpy.ops.(object.get_posicion)
    bl_label = "Driver Object Generator" # Nombre del operador
    bl_description = "Genera una trayectoria para el objeto seleccionado usando drivers para las coordenadas"

    def invoke(self, context, event):
        obj = context.object # Se guarda el objeto en la variable obj
        nombre_ob = obj.name # Se guarda el nombre del objeto en una variable
        modelo = obj.modelo # Se guarda el modelo en la variable modelo
        
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
                copiarFcurves(obj, car, "distancia_recorrida")
                copiarFcurves(obj, car, "distancia_deseada")
                
                car.scale = [10,10,10] # Escala el coche para que no sea tan pequeñp
                obj = car # Asigna el coche a la varible que pertenecia al anterior objeto
                
                delete(nombre_ob) # Borra el objeto anterior. (Función de prácticas anteriores)
        
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

        longitud_recorrida(obj)
            
        return {"FINISHED"}

def longitud_recorrida(obj):
    """
    Algoritmo para obtener la longitud del arco de la curva de movimiento

    Recorre todos los frames de la escena conviertiendolos en keyframes y calculando la distancia respecto al arco de la curva que les une.
    En blender se obtiene con la magnitud del vector del recorrido entre ambas posiciones.
    En teoría lo vimos como la resta del valor de las derivadas entre ambos puntosen valor absoluto sumado al valor ya acumulado

    Parameters
    ----------
    obj : object
        Objeto al que pertenece la curva.

    """
    # Asegurar que el objeto tiene datos de animación y una acción asignada
    if not obj.animation_data:
        obj.animation_data_create()
    if not obj.animation_data.action:
        obj.animation_data.action = bpy.data.actions.new(name="Distancia")

    obj.distancia_recorrida = 0.0  # Inicializa la distancia recorrida a 0 (creo que por el valor por defecto debería servir igualmente)
    distancia_acumulada = 0.0 # Inicialzia la distancia acumulada a 0 

    # Busca la fcurve donde se almacenará la distancia recorrida total
    fcurve = obj.animation_data.action.fcurves.find("distancia_recorrida")
    if not fcurve: # Si no esiste la fcurve se crea
        fcurve = obj.animation_data.action.fcurves.new(data_path="distancia_recorrida")

    """Línea recomendada por chatgpt"""
    fcurve.keyframe_points.clear()

    l_k = Vector([0, 0, 0]) #  Vector distancia recorrida inicializado
    
    # Recorre todos los frames de la escena
    """Existencia del frame_end descubierta por el profesor de laboratorio. El uso del range más el +1 dicho por chatgpt"""
    for k in range(bpy.context.scene.frame_start, bpy.context.scene.frame_end + 1):
        for c in range(3): # Obtiene el vector posicion usando las 3 coordenadas
            # El vector de la distancia recorrida se obtiene restando el vector de ambas posiciones
            l_k[c] = get_posicion(k + 1, obj, c) - get_posicion(k, obj, c)
        
        distancia_acumulada += l_k.length # Suma la magnitud del vector a la distancia recorrida
        obj.distancia_recorrida = distancia_acumulada # MEJOR PONER ESTO FUERA DEL BUCLE ??? Ni siquiera se si es necesario

        # Insertar un keyframe en la curva
        fcurve.keyframe_points.insert(k, distancia_acumulada) # Inserta en la fcurve de la distancia recorrida
        print(f"Insertado fotograma: {k} - Distancia acumulada: {distancia_acumulada}")
        
    #obj.distancia_recorrida = distancia_acumulada ???

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