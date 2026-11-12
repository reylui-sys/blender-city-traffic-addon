bl_info = {
    "name": "Orientación",
    "blender": (3, 0, 0),  # Asegúrate de que esto sea compatible con tu versión de Blender
    "category": "Object",
    "version": (1, 0, 0),
    "author": "Jose Luis León y compañeros del Grupo 06 (UV)",
    "description": "Addon para interpolar trayectorias y orientarlas",
    "location": "3D View > Tool Shelf > Algoritmos Orientación",
    "warning": "",
    "doc_url": "",
}

# Importa los módulos del addon
import bpy #type:ignore
from . import posicion
from . import operador_driver
from . import panel_driver

# Función para registrar todos los módulos del addon
def register():
    # Registra las clases del panel y el operador
    operador_driver.register()
    panel_driver.register()
    posicion.register()

# Función para anular el registro de los módulos del addon
def unregister():
    # Anula el registro de las clases del panel y el operador
    operador_driver.unregister()
    panel_driver.unregister()
    posicion.unregister()

# Esta línea asegura que el addon se registre cuando se instala
if __name__ == "__main__":
    register()
