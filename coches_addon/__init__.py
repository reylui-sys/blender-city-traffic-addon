bl_info = {
    "name": "CreacionCoches",
    "blender": (3, 0, 0),  # Asegúrate de que esto sea compatible con tu versión de Blender
    "category": "Object",
    "version": (1, 0, 0),
    "author": "Jose Luis León y compañeros del Grupo 06 (UV)",
    "description": "Addon para crear una ciudad con edificos y coches aleatorios",
    "location": "3D View > Tool Shelf > Creación de coches",
    "warning": "",
    "doc_url": "",
}

# Importa los módulos del addon
import bpy #type:ignore
from . import operador_driver
from . import posicion
from . import operador_borrar_ciudad
from . import operador_borrar_coches
from . import operador_ciudad
from . import operador_coche
from . import crear_coche
from . import panel_ciudad

# Función para registrar todos los módulos del addon
def register():
    # Registra las clases del panel y el operador
    operador_driver.register()
    
    operador_borrar_ciudad.register()
    operador_borrar_coches.register()
    operador_ciudad.register()
    operador_coche.register()
    crear_coche.register()
    panel_ciudad.register()

# Función para anular el registro de los módulos del addon
def unregister():
    # Anula el registro de las clases del panel y el operador
    operador_driver.unregister()
    
    operador_borrar_ciudad.unregister()
    operador_borrar_coches.unregister()
    operador_ciudad.unregister()
    operador_coche.unregister()
    crear_coche.unregister()
    panel_ciudad.unregister()


# Esta línea asegura que el addon se registre cuando se instala
if __name__ == "__main__":
    register()
