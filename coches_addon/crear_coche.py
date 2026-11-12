import bpy #type: ignore
from .borrar_elementos import delete as borrar_coches
from random import randint
from . import posicion
from .crear_ruta import crea_ruta

# Función para crear el coche. Se le pasa una lista con la posición del coche y la escena
def crear_coche(scene):
    
    # Almacena el número de calles
    nx = scene.n_calles_x
    ny = scene.n_calles_y
    
    # Almacena el ancho de la calle y de los edificios
    w = scene.ancho_calles
    l = scene.tam_manzana
    
    # Guarda la velocidad del coche (calles/seg) y la escala
    vel = scene.car_velocity
    scale = scene.car_scale
    h = scene.car_height
    
    # Genera una ruta con un número aleatorio de giros y el tamaño de la ciudad
    n_giros = randint(1, 3)  # Puedes ajustar el rango según sea necesario
    ruta = crea_ruta(n_giros, max(nx, ny))

    
    # Elige aleatoriamente una dirección (norte/sur, este/oeste)
    direccion = eleccionDireccion()
    
    # Frame auxiliar para crear la fcurve de la escena
    scene.keyframe_insert(data_path="scene_velocidad", frame=0)
    
    # En funcion de la direccion elegida se dispone a crear el coche con su trayectoria
    if direccion[0] == 0:
        
        if direccion[1] == 0:
            direccionar_norte_sur(nx, ny, l, w, vel, scale, h)
        else:
            direccionar_sur_norte(nx, ny, l, w, vel, scale, h)
             
    elif direccion[0] == 1:
        
        if direccion[1] == 0:
            direccionar_este_oeste(nx, ny, l, w, vel, scale, h)
        else:
            direccionar_oeste_este(nx, ny, l, w, vel, scale, h)

    # Suaviza la esfera
    bpy.ops.object.shade_smooth()
    
    obj = bpy.context.active_object
    
    #Asigna el nombre "Coche_x"
    obj.name = "Coche"
    
    tiempo = 0  # Empieza en el frame 0
    
    for i in range(len(ruta)):
        
        interseccion = ruta[i]
        
        # Establece la posición del coche en la intersección
        obj.location[0] = interseccion[0] * l + (2 * interseccion[0] - 1) * w / 2
        obj.location[1] = interseccion[1] * l + (2 * interseccion[1] - 1) * w / 2

        # Inserta fotograma clave para esta posición
        obj.keyframe_insert(data_path='location', frame=tiempo)
        
        """
    
        BORRADA PARTE HECHA POR CHAT GPT Y PUESTA UNA NUESTRA
        
        """

        # Si no es el último punto, calcula el tiempo al siguiente en función de la velocidad
        if i < len(ruta) - 1:
            siguiente_interseccion = ruta[i + 1]
            
            # Calcula la distancia en calles
            dx = (siguiente_interseccion[0] - interseccion[0])
            dy = (siguiente_interseccion[1] - interseccion[1])
            
            # Calcula la distancia euclidiana en términos de calles usando pitágoras
            distancia = (dx ** 2 + dy ** 2) ** 0.5
            
            # Calcula el tiempo en fotogramas usando velocidad en calles/seg
            tiempo += int((distancia / vel) * 24) # Incremento de tiempo en fotogramas

            """
            EJEMPLO PUESTO POR NOSTROS
            
            Si la siguiente intersección está a 4 calles de distancia y va a 2 calles/seg tardará 2 segundos
            (al estar en frames hace falta multplicar por 24).
            
            Así que si de una intersección a otra debe estar en x tiempo se debe sumar a la variable tiempo
            para ir acumulando y avanzando los keyframes
            
            """
    
    obj.frecuencia = scene.scene_frecuencia
    obj.amplitud = scene.scene_amplitud
    obj.eje = scene.scene_eje
    obj.oscilacion = scene.scene_oscilacion
    
    for i in range(3):
        obj.animation_data.action.fcurves.new(data_path="velocidad", index=i)
    
    bpy.ops.object.get_posicion()  # Llama al operador registrado para asignar drivers


# Funcion que elige aleatoriamente una dirección (norte/sur, este/oeste)
def eleccionDireccion():
    
    # Inicializa el string con la dirección (creo que se puede quitar)
    dir_inicio = ""

    # Elige aleatoriamente un valor entre 0 y 3
    rand = randint(0, 3)

    # Asigna en función del valor aleatorio una dirección
    if rand == 0:
        dir_inicio = "norte-sur"
    elif rand == 1:
        dir_inicio = "sur-norte"
    elif rand == 2:
        dir_inicio = "este-oeste"
    elif rand == 3:
        dir_inicio = "oeste-este"

    # Diccionario con dos valores para la dirección
    # el primer valor hace referencia a la dirección como tal,
    # el segundo valor indica el sentido de la dirección
    direccion =	{
        "norte-sur": [0, 0],
        "sur-norte": [0, 1],
        "este-oeste": [1, 0],
        "oeste-este": [1, 1]
    }
    
    # Print para hacer pruebas y ver que dirección se ha ejecutado
    print(direccion[dir_inicio])
    
    # Devuelve la dirección y el sentido elegidos
    return direccion[dir_inicio]

# Direcciona el coche y su trayectoria de norte - sur, es decir, del sur al norte
def direccionar_norte_sur(nx: int, ny: int, l: float, w: float, vel: float, scale: int, h: int):
    
    # Selecciona una calle aleatoriamente
    n = randint(1, nx - 1)
    
    # Genera una esfera (coche) en las coordenadas indicadas
    bpy.ops.mesh.primitive_uv_sphere_add(
        radius=1, 
        enter_editmode=False, 
        align='WORLD',
        # Al ser sur -> norte el coche comienza en una calle dirección X y en la posición Y = 0 (o su posicion inicial)
        location=((n * l + (n - 1) * w) + w/2, - l - w/2, h),
        # Coche 5 veces más pequeño que la calle ¿Debería ser una propiedad?
        scale=(w/scale, w/scale, w/scale)
    )
    """
    # Guarda el coche en una variable
    obj = bpy.context.active_object
    
    # Calcula el número de iteraciones en función de las calles y la velocidad
    # Se usa las calles horizontales porque es el eje perpendicular al eje X
    q = int((ny + vel)/vel)
    
    # Bucle que genera fotogramas clave cada segundo. El q + 1 es para asegurar que el coche que salga la ciudad
    for i in range(q + 1):
        
        # Añade keyframes cada 30 frames. Por ahora 30 se queda como placeholder
        obj.keyframe_insert(data_path='location',frame=i*24)
        
        # Desplaza en el eje Y de centro de calle a centro de calle siguiente
        obj.location[1] = (vel * i * l + (vel * 2 * i - 1) * w/2)
    """

# Direcciona el coche y su trayectoria de sur - norte, es decir, del norte al sur
def direccionar_sur_norte(nx: int, ny: int, l: float, w: float, vel: float, scale: int, h: int):
    
    # Selecciona una calle aleatoriamente
    n = randint(1, nx - 1)
    
    # Genera una esfera (coche) en las coordenadas indicadas
    bpy.ops.mesh.primitive_uv_sphere_add(
        radius=1, 
        enter_editmode=False, 
        align='WORLD',
        # Al ser norte -> sur el coche comienza en una calle dirección X y en la posición Y = última calle
        location=((n * l + (n - 1) * w) + w/2, (ny * l + (ny - 1) * w) + w/2, h),
        # Coche 5 veces más pequeño que la calle ¿Debería ser una propiedad?
        scale=(w/scale, w/scale, w/scale)
    )
    """
    # Guarda el coche en una variable
    obj = bpy.context.active_object

    # Calcula el número de iteraciones en función de las calles y la velocidad
    # Se usa las calles horizontales porque es el eje perpendicular al eje X
    q = int((ny + vel)/vel)
    
    # Bucle que genera fotogramas clave cada segundo. El q + 1 es para asegurar que el coche que salga la ciudad
    for i in range(q + 1):
        
        # Añade keyframes cada 30 frames. Por ahora 30 se queda como placeholder
        obj.keyframe_insert(data_path='location',frame=i*24)
        
        # Desplaza en el eje Y de centro de calle a centro de calle anterior
        obj.location[1] = obj.location[1] - vel * (l + w)
    """  
# Direcciona el coche y su trayectoria de este - oeste, es decir, del oeste al este
def direccionar_este_oeste(nx: int, ny: int, l: float, w: float, vel: float, scale: int, h: int):
    
    # Selecciona una calle aleatoriamente
    n = randint(1, ny - 1)
    
    # Genera una esfera (coche) en las coordenadas indicadas
    bpy.ops.mesh.primitive_uv_sphere_add(
        radius=1, 
        enter_editmode=False, 
        align='WORLD',
        # Al ser oeste -> este el coche comienza en una calle dirección X y en la posición Y = 0 (o su posicion inicial)
        location=( - l - w/2, (n * l + (n - 1) * w) + w/2, h),
        # Coche 5 veces más pequeño que la calle ¿Debería ser una propiedad?
        scale=(w/scale, w/scale, w/scale)
    )
    """v
    # Guarda el coche en una variable
    obj = bpy.context.active_object
    
    # Calcula el número de iteraciones en función de las calles y la velocidad
    # Se usa las calles horizontales porque es el eje paralelo al eje x
    q = int((nx + vel)/vel)
    
    # Bucle que genera fotogramas clave cada segundo. El q + 1 es para asegurar que el coche que salga la ciudad
    for i in range(q + 1):
        
        # Añade keyframes cada 30 frames. Por ahora 30 se queda como placeholder
        obj.keyframe_insert(data_path='location',frame=i*24)
        
        # Desplaza en el eje X de centro de calle a centro de calle siguiente
        obj.location[0] = (vel * i * l + (vel * 2 * i - 1) * w/2)
    """    
# Direcciona el coche y su trayectoria de oeste - este, es decir, del este al oeste
def direccionar_oeste_este(nx: int, ny: int, l: float, w: float, vel: float, scale: int, h: int):
    
    # Selecciona una calle aleatoriamente
    n = randint(1, ny - 1)
    
    # Genera una esfera (coche) en las coordenadas indicadas
    bpy.ops.mesh.primitive_uv_sphere_add(
        radius=1, 
        enter_editmode=False, 
        align='WORLD',
        # Al ser este -> oeste el coche comienza en una calle dirección Y y en la posición X = última calle
        location=((nx * l + (nx - 1) * w) + w/2, (n * l + (n - 1) * w + w/2), h),
        # Coche 5 veces más pequeño que la calle ¿Debería ser una propiedad?
        scale=(w/scale, w/scale, w/scale)
    )
    """
    # Guarda el coche en una variable
    obj = bpy.context.active_object
    
    # Calcula el número de iteraciones en función de las calles y la velocidad
    # Se usa las calles horizontales porque es el eje paralelo al eje x
    q = int((nx + vel)/vel)
    
    # Bucle que genera fotogramas clave cada segundo. El q + 1 es para asegurar que el coche que salga la ciudad
    for i in range(q + 1):
        
        # Añade keyframes cada 30 frames. Por ahora 30 se queda como placeholder
        obj.keyframe_insert(data_path='location',frame=i*24)
        
        # Desplaza en el eje X de centro de calle a centro de calle anterior
        obj.location[0] = obj.location[0] - vel * (l + w)
    """
# Funcion para registar el script de posicion
def register():
    posicion.register()

# Funcion para eliminar el script de posicion
def unregister():
    posicion.unregister()
    
if __name__ == "__main__": # Si el script es ejecutado directamente se llama a la función register.
 register()