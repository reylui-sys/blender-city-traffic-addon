import bpy #type: ignore
from . import borrar_elementos as borrar
from . import register
from . import city_gen
from importlib import reload

# Recarga los modulos usados si es necesario actualizar
reload(city_gen)
reload(register)

register.register() # Llama a la funcion register para registrar las propiedades

p = [0, 0]

# Numero de calles en el eje x y en el eje y
nx = bpy.context.scene.n_calles_x
ny = bpy.context.scene.n_calles_y

# Anchura de los edificios (l), anchura de las calles (w)
l = bpy.context.scene.tam_manzana
w = bpy.context.scene.ancho_calles

# Rango de valores para generar la altura aleatoria
min_h = bpy.context.scene.alt_edif_min
max_h = bpy.context.scene.alt_edif_max

# Funcion que elimina los edificios, las "manzanas" ya existentes
borrar.delete("Manzana")

# Llamada a la funcion para crear la ciudad
city_gen.create_city(p, nx, ny, l, w, min_h, max_h)