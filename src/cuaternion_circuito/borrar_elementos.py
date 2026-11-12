import bpy #type: ignore

"""
borrar_elemetos.py

Algoritmo para borrar objetos en blender con un determinado nombre.

Autores: Jose Luis León y compañeros del Grupo 06 (Animación, Grado en Ingeniería Multimedia, UV).
"""

# Define la funcion
def delete(str):    
    """
    Selecciona los objetos en blender con un determinado nombre y los cierra
    
    Parameters
    ----------
    str : string
        Nombre de los objetos a borrar.
    """
    # Deselecciona todos los objetos
    bpy.ops.object.select_all(action='DESELECT')
    
    # Bucle que pasa por todos los objetos de la escena
    for obj in bpy.data.objects:
        
        # Si detecta el que empieza por el string deseado lo selecciona
        if obj.name.startswith(str):
            obj.select_set(True)
            
    # Elimina los seleccionados      
    bpy.ops.object.delete()