import bpy # type: ignore

# Definición de la clase que extiende del tipo Panel para crear un panel
class DriverPanel(bpy.types.Panel):
    """Crea un panel para seleccionar un método de interpolación y sus propiedades"""
    bl_label = "Driver Control" # Nombre de la clase. Aparece en el título del panel
    bl_idname = "OBJECT_PT_DriverControl" # Identificador del panel con kla convención OBJECT_PT_
    bl_space_type = 'VIEW_3D' # Se añadirá al espacio de trabajo de la vista en 3D (otros ejemplos "PROPERTIES", "TEXT_EDITOR"...)
    bl_region_type = 'UI' # Dentro del espacio de trabajo se añadirá a la barra lateral (otros ejemplos "TOOLS", "HEADER", "WINDOW"...)
    bl_category = "Driver Control" # Nombre de la pestaña de la barra UI

    def draw(self, context):
        layout = self.layout #Guarda la instancia del panel en una variable
        # Separa el nombre de las variables de las cajas de los valores y quita decoración extra
        layout.use_property_split = True
        layout.use_property_decorate = False
        obj = context.object # Guarda el objeto en una variable (para poder usas sus propiedades)

        row = layout.row() # Crea una fila
        row.label(text="Generación trayectoria interpolada", icon='DRIVER') # Da nombre e icono a una fila
        
        layout.prop(obj, "metodo", text="Método de interpolación") # Muestra la propiedad EnumProp (el desplegable)
        row = layout.row()
        
        # Se comprueba que método se ha elegido, se muestran las propiedades pertinentes y se actualiza el operador
        if obj.metodo == 'LN':
            # Guarda que método es para actualizar el operador
            metodo_texto = "Crear trayectoria Lineal"
        elif obj.metodo == 'HRMT':
            row = layout.row()
            row.label(text="Velocidades", icon='HANDLE_VECTOR')
            # Muestra la propiedad de la velocidad
            row.prop(obj, "velocidad", text='')
            # Guarda que método es para actualizar el operador
            metodo_texto = "Crear trayectoria de Hermite"
        elif obj.metodo == 'C-R':
            row = layout.row()
            row.label(text="Tensión", icon='HANDLE_VECTOR')
            # Muestra la propiedad de la tensiñon
            layout.prop(obj, "tension", text="")
            # Guarda que método es para actualizar el operador
            metodo_texto = "Crear trayectoria de Catmull-Rom"
        # Genera el operador
        row = layout.row()
        row.operator("object.get_posicion", text=metodo_texto)
            

def register():
    bpy.utils.register_class(DriverPanel) # Registra la clase del panel
    # Se crea y registra la propiedad de enumeracion, con su nombre, su lista de itemas, descripción y valor por defecto
    bpy.types.Object.metodo = bpy.props.EnumProperty(
        name="metodo",
        description="Selecciona una interpolación",
        # ID del item, etiqueta que se muestra al usuario, descripción
        items=[
            ('LN', "Lineal", "Esto es la opción Lineal"),
            ('HRMT', "Hermite", "Esto es la opción de Hermite"),
            ('C-R', "Catmull-Rom", "Esto es la opción de Catmull-Roll")
        ],
        default='LN',  # Valor por defecto
    )
    # Registra la propiedad del vector velocidad
    bpy.types.Object.velocidad = bpy.props.FloatVectorProperty(name="velocidad", description='Vector velocidades de Hermite', default=(0.0, 0.0, 0.0), min=-10.0, max=10.0, size=3)
    # Registra la propiedad de tensión
    bpy.types.Object.tension = bpy.props.FloatProperty(name="Tensión", description="Tensión para Catmull-Rom", default=2, min=0.0, max=10.0)
    # Registra la propiedad keyframe que se usará para poder almacenar el keyframe siguiente al frame actual
    bpy.types.Object.keyframe = bpy.props.IntProperty(name="keyframe", description="Fotograma clave siguiente")
    
def unregister():
    bpy.utils.unregister_class(DriverPanel) # Elimina del registro la clase del panel
    del bpy.types.Object.metodo # Elimina la propiedad de enumeracion
    del bpy.types.Object.velocidad # Elimina la propiedad del vector de velocidad
    del bpy.types.Object.tension  # Elimina la propiedad de la tensión
    del bpy.types.Object.keyframe  # Elimina la propiedad auxiliar keyframe
    
if __name__ == "__main__": # Si el script es ejecutado directamente se llama a la función register.
    register()