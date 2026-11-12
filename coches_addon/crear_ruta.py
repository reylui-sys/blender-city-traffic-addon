import bpy #type: ignore
from random import choice

def crea_ruta(nturns : int, N: int):
    
    calles = set(range(N+1))
    
    i = 0
    j = 0
    posns = []
    # Elegimos al azar si  laprimera posicion es en fila o columna
    fila = choice([True, False])
    
    for turn in range(nturns + 1):
        if fila:
            fila = False
            # Eleccion aleatoria de la siguiente calle
            i = choice(list(calles - {i}))
        else:
            fila = True
            #Eleccion aleatoria de la siguiente calle
            j = choice(list(calles - {j}))
        posns.append([i, j])
    # Forzamos que acabe enla ultima calle
    if fila:
        i = N
    else:
        j = N
        
    posns.append([i, j])
    
    return posns