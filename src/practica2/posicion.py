import bpy #type: ignore
from interpola import interpola_valores as interpolar
from mathutils import noise #type: ignore

# Funcion para obtener la posicion de un objeto en un frame determinado
def get_posicion(frm : float, obj : object, coord : int):
    # Asigna la lista de las curvas location en una variable
    lista_keyframes = obj.animation_data.action.fcurves.find('location', index=coord).keyframe_points
    i = 0 # Iterador para el bucle
    # Bucle que busca por los fotogramas clave de la curva location el que sea mayor al frame actual
    while i < len(lista_keyframes) and lista_keyframes[i].co[0] < frm:
        i += 1
    '''
    Si i = 0 la posición es la del primer keyframe, si i llega al final
    de la lista la posición es la del último.
    En caso contrario se calcula con la interpolación lineal.
    
    co[0] -> Número del keyframe (f)
    co[1] -> Valor del keyframe (p)
    '''
    if i == 0:
        pos = lista_keyframes[0].co[1]
    elif i == len(lista_keyframes):
        pos = lista_keyframes[i - 1].co[1]
    else:
        keyframe1 = lista_keyframes[i - 1].co[0]
        keyframe2 = lista_keyframes[i].co[0]
        valor1 = lista_keyframes[i - 1].co[1]
        valor2 = lista_keyframes[i].co[1]
        # Asigna a la propiedad keyframe del objeto el keyframe siguiente al frame actual
        obj.keyframe = i
        # llama a la función para interpolar
        pos = interpolar(frm, keyframe1, keyframe2, valor1, valor2, obj, coord)
        
        frec = obj.frecuencia
        amp = obj.amplitud
        osc = obj.oscilacion
        eje = obj.eje
        
        if eje == "EX":
            eje_num = 0
        elif eje == "EY":
            eje_num = 1
        elif eje == "EZ":
            eje_num = 2
        
        
        
        if osc and coord == eje_num:
            pos += amp * noise.noise([obj.location[0] * frec, obj.location[1] * frec, obj.location[2] * frec], noise_basis='PERLIN_ORIGINAL')
            
    return pos

def register():
    # Registra la función en el namespace de los drivers
    bpy.app.driver_namespace['get_pos'] = get_posicion

def unregister():
    # Elimina la función en el namespace de los drivers
    del bpy.app.driver_namespace['get_pos']
    
def asigna_driver_posicion(obj,coord):
    # Creamos el driver en la coordenada elegida. El driver se queda
    # guardado en la variable drv
    drv = obj.driver_add('location',coord).driver
    # Habilitamos la posibilidad de que reciba el propio objeto, que
    # necesitaremos para acceder a los fotogramas clave.
    drv.use_self = True
    # Asignamos la expresión que queremos que se utilice.
    # Se está utilizando una "f-string" para constuir una cadena
    # a partir del valor de las variables coord y method
    drv.expression = f"get_pos(frame, self, {coord})"
    
if __name__ == "__main__": # Si el script es ejecutado directamente se llama a la función register.
 register()
 #  Bucle para asignar los drivers a cada coordenada
 for c in range(3):
     asigna_driver_posicion(bpy.context.active_object, c)