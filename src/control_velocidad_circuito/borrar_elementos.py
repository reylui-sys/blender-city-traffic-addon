import bpy #type: ignore

# Define la funcion
def delete(str):    
    
    # Deselecciona todos los objetos
    bpy.ops.object.select_all(action='DESELECT')
    
    # Bucle que pasa por todos los objetos de la escena
    for obj in bpy.data.objects:
        
        # Si detecta el que empieza por el string deseado lo selecciona
        if obj.name.startswith(str):
            obj.select_set(True)
            
    # Elimina los seleccionados      
    bpy.ops.object.delete()