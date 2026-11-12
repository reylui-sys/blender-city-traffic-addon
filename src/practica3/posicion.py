import bpy #type: ignore
from interpola import interpola_valores as interpolar
from mathutils import Vector #type: ignore
from mathutils import Quaternion #type: ignore

"""
posicion.py

Algoritmos para obtener la posición y el cuaternión del objeto

Autores: Jose Luis León y compañeros del Grupo 06 (Animación, Grado en Ingeniería Multimedia, UV).
"""

# Funcion para obtener la posicion de un objeto en un frame determinado
def get_posicion(frm : float, obj : object, coord : int):
    """
    Algoritmo para obtener la posición del objeto y los datos para
    interpolar
    
    Obtiene la lista de keyframes location, llega al frame actual y llama
    a la función interpolar
    
    Parameters
    ----------
    frm : float
        Frame Actual.
    obj : object
        Objecto a interpolar su posición.
    coord : int
        Coordenada correspondiente a interpolar.

    Returns
    -------
    float
        La posición interpolada.
    """
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
        
    return pos
"""
v1 = e1.cross(t).normalized()

ang = e1.angle(t)

real = math.cos(ang/2)

# Importante importar el módulo "math"
vi = math.sin(ang/2) * v1[0]
vj = math.sin(ang/2) * v1[1]
vk = math.sin(ang/2) * v1[2]

imaginaria = Vector([vi, vj, vk])


q = Vector([real, imaginaria])

q1 = Quaternion((real,vi,vj,vk))
q1_2 = Quaternion(v1, ang)
"""

def get_lat_vec(t: Vector) -> Vector:
    """
    Algoritmo para obtener el vector lateral y horizontal
    
    Usa el vector en el eje Z para que el producto vectorial sea sí o sí
    perpendicular y por tanto sea horizontal
    
    Parameters
    ----------
    t : Vector
        Vector tangente del que se quiere calcular su lateral.

    Returns
    -------
    Vector
        Vector lateral calculado.
    """
    # Vector auxiliar que representa el eje Z.
    # Con el fin de que al hacer el producto escalar esa componente Z de 0 dejándolo horizontal
    z = Vector([0,0,1])
    
    # Producto escalar del vector tangente con el eje Z para obtener el vector horizontal y perpendicular al tangente
    l = z.cross(t).normalized()
    
    return l

""" Preguntar si es válida esta opción

def get_lat_vec(t: Vector) -> Vector:
    
    return Vector([0,0,1]).cross(t).normalized()
    
"""

def get_up_vec(t: Vector) -> Vector:
    """
    Algoritmo para obtener el vector UP
    
    Usa el vector lateral para calcular su perpendicular, que será hacía arriba
    
    Parameters
    ----------
    t : Vector
        Vector tangente del que se quiere calcular su UP.

    Returns
    -------
    Vector
        Vector UP calculado.
    """
    # Obtiene el vector lateral llamando a la función previa
    l = get_lat_vec(t)
    
    # Calcula el vector perpendicular al tangente y el lateral con el producto vectorial
    up = t.cross(l).normalized()
    
    return up

""" Preguntar si es válida esta opción

def get_up_vec(t: Vector) -> Vector:
    
   return t.cross(get_lat_vec(t)).normalized()
   
"""

def get_quat_from_vecs(e: Vector, t: Vector) -> Quaternion:
    """
    Algoritmo para obtener el cuaternión que orienta e con t
    
    Obtiene el vector perpendicular a ambos y su angulo con el arcocoseno
    para calcular el cuaternión
    
    Parameters
    ----------
    e : Vector
        Vector unitario del eje del objeto que se quiere orientar.
    t : Vector
        Vector tangente al que se quiere orientar.

    Returns
    -------
    Quaternion
        Quaternion que orienta e con t.
    """
    # Vector perpendicular al e y t que se usará como eje de rotación del cuaternión
    v1 = e.cross(t).normalized()
    
    # Si el vector resultante es nulo el angulo vale 0.
    # De lo contrario se calcula el ángulo entre ambos
    if v1.magnitude == 0:
        ang = 0
        
    else:
        # Ángulo entre ambos vectores para saber cuantos radianes rotar
        ang = e.angle(t)
    
    # Instancia el quaternion con el eje y el ángulo calculados
    q = Quaternion(v1, ang)
    
    return q

""" Preguntar si es válida esta opción

def get_quat_from_vecs(e: Vector, t: Vector) -> Quaternion:
    
    return Quaternion(e.cross(t).normalized(), e.angle(t))
    
"""

def get_quat_rot(t: Vector, e1: Vector, e3: Vector, ang: float) -> Quaternion:
    """
    Algoritmo para obtener el cuaternión que orienta e con t y su vector UP
    
    Hace lo mismo que el anterior pero usa su vector UP para que el objeto no rote
    lateralmente. Además permite controlar esa rotación con un ángulo
    
    Parameters
    ----------
    t : Vector
        Vector tangente al que se quiere orientar.
    e1 : Vector
        Vector unitario del eje del objeto que se quiere orientar.
    e3 : Vector
        Vector unitario al que se quiere orientar el vector UP.
    ang : float
        Ángulo para darle a la rotación lateral.

    Returns
    -------
    Quaternion
        Quaternion que orienta e con t.
    """
    # Obtiene el vector up del tangente (el up de la trayectoria)
    up = get_up_vec(t)

    # Calcula el primer cuaternion que orienta el vector e1 con el tangente
    q1 = get_quat_from_vecs(e1, t)

    # Calcula el vector e3' fruto de aplicar a e3 el cuaternión anterior
    e3_prima = q1 @ e3

    # Calcula un nuevo cuaternión con el vector e3' y el up para orientar el "up" del objeto con el up de la trayectoria
    q2 = get_quat_from_vecs(e3_prima, up)
    
    # Calcula un nuevo cuaternion con el angulo elegido para un control lateral. 
    # Usa el tangente como eje de rotación para que sea rotación lateral
    q3 = Quaternion(t, ang)


    # Multiplica los cuaterniones para formar uno nuevo compuesto
    q = q3 @ q2 @ q1
    
    return q

""" Preguntar si es válida esta opción

def get_quat_rot(t: Vector, e1: Vector, e3: Vector, ang: float) -> Quaternion:
    
    return get_quat_from_vecs(e1, t) @ get_quat_from_vecs(get_quat_from_vecs(e1, t) @ e3, get_up_vec(t)) @ Quaternion(t, ang)
    
"""


"""
VERSIÓN DIFERENTE CAMBIANDO EL COMO SE CALCULA EL VECTOR NUEVO.
USANDO LA FUNCIÓN ROTATE SE MODIFICA DIRECTAMENTE EL VECTOR


def get_quat_rot(t: Vector, e1: Vector, e3: Vector, ang: float) -> Quaternion:
    
    up = get_up_vec(t)
    
    q1 = get_quat_from_vecs(e1, t)
    
    e3.rotate(q1)
    
    q2 = get_quat_from_vecs(e3, up)
    
    q3 = Quaternion(t, ang)
    
    q = q1 @ q2 @ q3
    
    return q
"""

def get_quaternion(frame: float, obj: object, coord: int) -> float:
    """
    Algoritmo para obtener el cuaternión

    Esta técnica de interpolación es la más básica para definir un rango de la valores
    en dos puntos conocidos. Consiste en trazar una recta entre dichos puntos y obtener
    los valores intermedios de ahí.

    Parameters
    ----------
    frame : float
        Frame Actual.
    obj : object
        Objeto que se quiere orientar.
    coord : int
        Índice del componente para retornar.

    Returns
    -------
    float
        Contenido de una componente del cuaternión.
    """
    # Inicializa el vector tangente y el siguiente
    d = Vector()
    d_2 = Vector()

    # Obtiene el vector tangente como la diferencia de los vectores posiciones contiguos
    for i in range(3):
        # Se podría hacer como frame - frame-1
        pos_sig = get_posicion(frame + 1, obj, i)
        pos_actual = get_posicion(frame, obj, i)
        
        pos_sig_2 = get_posicion(frame + 3, obj, i)
        pos_actual_2 = get_posicion(frame + 2, obj, i)

        # Asigna una componente del vector tangente
        d[i] = pos_sig - pos_actual
        # Calcula el siguiente vector tangente para calular un angulo proporcional al giro
        d_2[i] = pos_sig_2 - pos_actual_2

    # Normaliza el vector tangente y el siguiente
    u = d.normalized()
    u_2 = d_2.normalized()

    # Obtiene el eje del objeto que se quiere orientar en la dirección de la trayectoria
    orientacion = obj.orientacion

    # Según el eje obtenido se asigna un vector adecuado
    if orientacion == "ORX":
        e = Vector([1,0,0])
    elif orientacion == "ORY":
        e = Vector([0,1,0])
    elif orientacion == "ORZ":
        e = Vector([0,0,1])
    elif orientacion == "OR-X":
        e = Vector([-1,0,0])
    elif orientacion == "OR-Y":
        e = Vector([0,-1,0])
    elif orientacion == "OR-Z":
        e = Vector([0,0,-1])
        

    angP = u.angle(u_2) # Ángulo entre el vector tangente actual y el siguiente. P de proporcional al giro.
        
    """
    SI SE QUIERE USAR EL CONTROL LATERAL DE FORMA NORMAL USA LA PRIMERA Q
    SI SE QUIERE USAR EL CONTROL LATERAL DEL EJERCICIO ADICIONAL EN FUNCION DE LA CURVA USA LA SEGUNDA Q
    
    """
    # q = get_quat_rot(u, e, get_up_vec(e) , obj.alabeo) # Calcula el cuaternion de rotación final
    q = get_quat_rot(u, e, get_up_vec(e) , -angP * obj.alabeo / obj.tension) # Calcula el cuaternion de rotación final
    
    return q[coord] # Devuelve la componente del cuaternión correspondiente


def register():
    # Registra la función en el namespace de los drivers
    bpy.app.driver_namespace['get_pos'] = get_posicion
    bpy.app.driver_namespace['get_quat'] = get_quaternion

def unregister():
    # Elimina la función en el namespace de los drivers
    del bpy.app.driver_namespace['get_pos']
    del bpy.app.driver_namespace['get_quat']
    
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
    
def asigna_driver_cuaternion(obj: object, d: int):
    # Creamos el driver en la coordenada elegida. El driver se queda
    # guardado en la variable drv
    drv = obj.driver_add('rotation_quaternion',d).driver
    # Habilitamos la posibilidad de que reciba el propio objeto, que
    # necesitaremos para acceder a los fotogramas clave.
    drv.use_self = True
    # Asignamos la expresión que queremos que se utilice.
    # Se está utilizando una "f-string" para constuir una cadena
    # a partir del valor de las variables d y method
    drv.expression = f"get_quat(frame, self, {d})"
    
if __name__ == "__main__": # Si el script es ejecutado directamente se llama a la función register.
 register()
 #  Bucle para asignar los drivers a cada coordenada
 for c in range(3):
     asigna_driver_posicion(bpy.context.active_object, c)
     
 # Comprueba si se ha habilitado la rotación
 if bpy.context.active_object.rotacion == True:
     # Cambia el modo de rotación
     bpy.context.active_object.rotation_mode = 'QUATERNION'
     # Bucle que asigna el driver a cada componente del cuaternión
     for d in range(4):
         asigna_driver_cuaternion(bpy.context.active_object, d) # Llama 4 veces a la función asigna driver