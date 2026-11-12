import bpy #type: ignore

"""
interpola.py

Algoritmos de interpolación

Autores: Jose Luis León y compañeros del Grupo 06 (Animación, Grado en Ingeniería Multimedia, UV).
"""

def lineal(t: float, t0: float, t1: float, x0: float, x1: float):
    """
    Algoritmo de interpolación lineal

    TODO: Implementar
    TODO: Documentar
    
    Esta técnica de interpolación es la más básica para definir un rango de la valores
    en dos puntos conocidos. Consiste en trazar una recta entre dichos puntos y obtener
    los valores intermedios de ahí.

    Parameters
    ----------
    t : float
        Frame Actual.
    t0 : float
        Keyframe anterior.
    t1 : float
        Keyframe siguiente.
    x0 : float
        Valor del keyframe anterior.
    x1 : float
        Valor del keyframe siguiente.

    Returns
    -------
    float
        La posición en función lineal.
    """
    # Cálculo del término u
    u = (t - t0) / (t1 - t0)
    # Cálculo de la posición
    pos = x0 + (x1 - x0) * u
    return pos

def hermite(t: float, t0: float, t1: float, x0: float, x1: float, obj: object, coord: int):
    """
    Algoritmo de interpolación de Hermite

    TODO: Implementar
    TODO: Documentar
    
    El algoritmo de Hermite permite interpolar usando la posición de unos puntos cocnretos
    junto a las velocidades de los mismo. Es una interpolación útil pero para la animación
    no es conveniente puesto que conocer la velocidad en cada punto es difícil y nada instuitivo.

    Parameters
    ----------
    t : float
        Frame Actual.
    t0 : float
        Keyframe anterior.
    t1 : float
        Keyframe siguiente.
    x0 : float
        Valor del keyframe anterior.
    x1 : float
        Valor del keyframe siguiente.
    obj : object
        Objeto "self" que está siendo interpolado
    coord : int
        Coordenada actual

    Returns
    -------
    float
        La posición en función de Hermite.
    """
    # Cálculo del término u
    u = (t - t0) / (t1 - t0)
    # Cálculo de u^2
    u2 = u * u
    # Cálculo de u^3
    u3 = u2 * u
    # Asigna a la variable i el keyframe siguiente del frame actual
    i = obj.keyframe
    # Cálculo de las velocidades
    velocidades = obj.animation_data.action.fcurves.find('velocidad', index=coord).keyframe_points
    v0 = velocidades[i].co[1]
    v1 = velocidades[i - 1].co[1]
    # Cálculo de los coeficientes para simplificar la función
    h1 = 1 - 3 * u2 + 2 * u3
    h2 = u2 * (3 - 2 * u) 
    h3 = u * (u - 1) * (u - 1)
    h4 = u2 * (u - 1)
    # Cálculo de la posición
    pos = h1 * x0 + h2 * x1 + h3 * v0 + h4 * v1
    return pos

def catmull_rom(t: float, t0: float, t1: float, x0: float, x1: float, obj: object, coord: int):
    """
    Algoritmo de interpolación de Catmull-Rom

    TODO: Implementar
    TODO: Documentar
    
    Este algoritmo de interpolación soluciona el "problema" de Hermite en el mundo de la animación.
    Aquí la velocidad se calcula por detrás, quitandole la responsabilidad al usuario excepto por un valor
    "tau" que sirve para ajustar la "tensión" de la curva, influyendo en su forma.

    Parameters
    ----------
    t : float
        Frame Actual.
    t0 : float
        Keyframe anterior.
    t1 : float
        Keyframe siguiente.
    x0 : float
        Valor del keyframe anterior.
    x1 : float
        Valor del keyframe siguiente.
    obj : object
        Objeto "self" que está siendo interpolado
    coord : int
        Coordenada actual

    Returns
    -------
    float
        La posición en función de Catmull-Rom.
    """
    # Cálculo del término u
    u = (t - t0) / (t1 - t0)
    # Cálculo de u^2
    u2 = u * u
    # Cálculo de u^3
    u3 = u2 * u
    # Cálculo de los coeficientes para simplificar la función
    h1 = 1 - 3 * u2 + 2 * u3
    h2 = u2 * (3 - 2 * u) 
    h3 = u * (u - 1) * (u - 1)
    h4 = u2 * (u - 1)
    # Asigna a la variable tau la tensión seleccionada
    tau = obj.tension
    # Asigna a la variable i el keyframe siguiente del frame actual
    i = obj.keyframe
    # Obtiene la lista de los keyframes de la coordenada coord
    fotogramas = obj.animation_data.action.fcurves.find('location', index=coord).keyframe_points
    # Se comprueba si se está en el primer punto o el penúltimo
    if i == 1:
        vi = fotogramas[i + 1].co[1] - fotogramas[i - 1].co[1]
        vi_1 = fotogramas[1].co[1] - fotogramas[0].co[1] # La velocidad del punto anterior del primero corresponde a v0 = τ(p1 −p0);
    elif i == len(fotogramas) - 1:
        vi = fotogramas[len(fotogramas) - 1].co[1] - fotogramas[i - 1].co[1] # La velocidad del punto siguiente al penúltimo corresponde a vn = τ(pn −pn−1)
        vi_1 = fotogramas[i].co[1] - fotogramas[i - 2].co[1]
    else:
        # En caso de no ser ninguno de esos se calcula en base al keyframe siguiente y anterior. vi = τ(pi+1 −pi−1)
        vi = fotogramas[i + 1].co[1] - fotogramas[i - 1].co[1]
        vi_1 = fotogramas[i].co[1] - fotogramas[i - 2].co[1]
    # Cálculo de la posición
    pos = h1 * x0 + h2 * x1 + h3 * tau * vi_1 + h4 * tau * vi 
    return pos

def interpola_valores(t: float, t0: float, t1: float, x0: float, x1: float, obj: object, coord: int):
    """
    Selección de interpolación a usar

    TODO: Implementar
    TODO: Documentar

    Parameters
    ----------
    t : float
        Frame Actual.
    t0 : float
        Keyframe anterior.
    t1 : float
        Keyframe siguiente.
    x0 : float
        Valor del keyframe anterior.
    x1 : float
        Valor del keyframe siguiente.
    obj : object
        Objeto "self" que está siendo interpolado
    coord : int
        Coordenada actual

    Returns
    -------
    float
        La posición del objeto en el frame actual.
    """
    pos = 0.0 # Inicialización de la variable de la posición
    metodo = obj.metodo # Almacena el método elegido
    keyframe = obj.keyframe # Almacena el keyframe siguiente al frame actual
    # Según el método elegido se llama a una función u otra
    if metodo == 'LN':
        pos = lineal(t, t0, t1, x0, x1)
    elif metodo == 'HRMT':
        pos = hermite(t, t0, t1, x0, x1, obj, coord)
    elif metodo == 'C-R':
        pos = catmull_rom(t, t0, t1, x0, x1, obj, coord)

    return pos