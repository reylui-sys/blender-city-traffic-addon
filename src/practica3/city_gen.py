import bpy # type: ignore
import random
import math

def create_city(p, nx, ny, l, w, min_h, max_h):
    # Guarda el valor del centro de la ciudad    
    # c = centro_ciudad(nx, ny, l, w, p)
    
    # Bucle que itera sobre toda la malla donde estarán los edificios en funcion del numero de calles en el eje x e y y crea el edificio
    for i in range(nx):
        for j in range(ny):
            # Declara la altura aleatoriamente
            h = random.uniform(min_h, max_h)
            # Funcion para calcular la posicion del centro de cada edificio
            b = [p[0] + (i*(l + w) + l/2), p[1] + (j*(l + w) + l/2), h]
                
            # Genera el cubo que será el edificio
            bpy.ops.mesh.primitive_cube_add(
                size=2,
                enter_editmode=False,
                align='WORLD', 
                location=b, # Vector calculado previamente
                scale=(1, 1, h) # Escala de cada edificio, en x e y tendrá la misma anchura y la altura será h
            )
            # Asigna a una variable el objeto activo y le cambia el nombre a Manzana
            obj = bpy.context.active_object
            obj.name = "Manzana"
            
            obj.scale = (l/2, l/2, 1)

    
def probabilidad_edificio(x, y):
    # Calcula la distancia al origen del punto (x, y)
    dist = math.sqrt(x**2 + y**2)
    # Calcula y devuelve la probabilidad de edificio para ese punto
    #prob = math.tanh(-0.4*(dist - 12))*0.45 + 0.5
    prob = math.tanh(-0.4*(dist-12))*0.45 + 0.2
    return prob


def centro_ciudad(nx, ny, l, w, p):
    # Calcula la longitud al punto medio en x e y
    dx = nx*l + (nx - 1)*w
    dy = ny*l + (ny - 1)*w
    # Calcula el centro de la ciudad
    c = [p[0] + dx/2, p[1] + dy/2, 0] 
    return c