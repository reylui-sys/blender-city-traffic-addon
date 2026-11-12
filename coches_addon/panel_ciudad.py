import bpy # type: ignore

# Definición de la clase que extiende del tipo Panel para crear un panel
class ProceduralCityPanel(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Ciudad Procedural: Parametros" # Nombre de la clase. Aparece en el título del panel
    bl_idname = "OBJECT_PT_ProceduralCity" # Identificador del panel con kla convención OBJECT_PT_
    bl_space_type = 'VIEW_3D' # Se añadirá al espacio de trabajo de la vista en 3D (otros ejemplos "PROPERTIES", "TEXT_EDITOR"...)
    bl_region_type = 'UI' # Dentro del espacio de trabajo se añadirá a la barra lateral (otros ejemplos "TOOLS", "HEADER", "WINDOW"...)
    bl_category = "Procedural City" # Nombre de la pestaña de la barra UI

    def draw(self, context):
        layout = self.layout #Guarda la instancia del panel en una variable
        
        # Separa el nombre de las variables de las cajas de los valores y quita decoración extra
        layout.use_property_split = True
        layout.use_property_decorate = False

        scene = context.scene # Guarda la escena en una variable (para poder usas sus propiedades)
        obj = context.object

        row = layout.row() # Crea una fila
        row.label(text="Creacion del suelo", icon='WORLD_DATA') # Da nombre e icono a una fila

        col = layout.column() # Crea una columna
        
        # Añade propiedades a la columna de la escena
        col.prop(scene, "n_calles_x")
        col.prop(scene, "n_calles_y")
        col.prop(scene, "ancho_calles")
        
        # Añade espacios y una fila
        layout.separator()
        row = layout.row()
        
        row.label(text="Creacion de los edificios", icon='MOD_BUILD')
        col = layout.column()
        col.prop(scene, "tam_manzana")
        col.prop(scene, "alt_edif_min")
        col.prop(scene, "alt_edif_max")
        
        layout.separator()
        row = layout.row()
        
        
        """
        row = layout.row() # Crea una fila
        row.label(text="Oscilación del coche", icon='MESH_ICOSPHERE') # Da nombre e icono a una fila
        col = layout.column()
        col.prop(obj, "oscilacion", text="Aplicar oscilación")
        
        if obj.oscilacion == True:
            col.prop(obj, "frecuencia", text="Frecuencia")
            col.prop(obj, "amplitud", text="Amplitud")
            col.prop(obj, "eje", text="Eje de oscilación")
        
        layout.separator()
        row = layout.row() # Crea una fila
        """
        
        # Añade el botón que ejecuta el operador. Haciendo referencia al operaodor "bpy.ops.object.gen_ciudad"
        row.operator("object.gen_ciudad", text="Generar Ciudad")
        row.operator("object.delete_city", text="Borrar Ciudad")

class CarGenerator(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Generador de coche: Parametros" # Nombre de la clase. Aparece en el título del panel
    bl_idname = "OBJECT_PT_CarGenerator" # Identificador del panel con kla convención OBJECT_PT_
    bl_space_type = 'VIEW_3D' # Se añadirá al espacio de trabajo de la vista en 3D (otros ejemplos "PROPERTIES", "TEXT_EDITOR"...)
    bl_region_type = 'UI' # Dentro del espacio de trabajo se añadirá a la barra lateral (otros ejemplos "TOOLS", "HEADER", "WINDOW"...)
    bl_category = "Procedural City" # Nombre de la pestaña de la barra UI

    def draw(self, context):
        layout = self.layout #Guarda la instancia del panel en una variable
        
        # Separa el nombre de las variables de las cajas de los valores y quita decoración extra
        layout.use_property_split = True
        layout.use_property_decorate = False

        scene = context.scene # Guarda la escena en una variable (para poder usas sus propiedades)

        row = layout.row() # Crea una fila
        row.label(text="Creacion de un coche", icon='MATERIAL') # Da nombre e icono a una fila
        
        col = layout.column() # Crea una fila
        
        # Añade propiedades a la columna de la escena
        col.prop(scene, "car_velocity")
        col.prop(scene, "car_scale")
        col.prop(scene, "car_height")
        
        layout.separator() 
        
        # Crea una columna
        col = layout.column()
        layout.separator()
        
        col.prop(scene, "ncoches", text="Número de coches")
        
        # Añade propiedades a la columna de la escena
        col.prop(scene, "scene_metodo", text="Método")   
        
        # Se comprueba que método se ha elegido, se muestran las propiedades pertinentes y se actualiza el operador
        if scene.scene_metodo == 'LN':
            
            # Guarda que método es para actualizar el operador
            metodo_texto = "Lineal"
            
        elif scene.scene_metodo == 'HRMT':
            
            col.prop(scene, "scene_velocidad", text="Velocidad")
            
            # Guarda que método es para actualizar el operador
            metodo_texto = "Hermite"
            
        elif scene.scene_metodo == 'C-R':
            
            col.prop(scene, "scene_tension", text="Tensión")
            
            metodo_texto = "Catmull-Rom"
        
        layout.separator()
        row = layout.row()
        
        row = layout.row() # Crea una fila
        row.label(text="Oscilación del coche", icon='MESH_ICOSPHERE') # Da nombre e icono a una fila
        col = layout.column()
        col.prop(scene, "scene_oscilacion", text="Aplicar oscilación")
        
        if scene.scene_oscilacion == True:
            col.prop(scene, "scene_frecuencia", text="Frecuencia")
            col.prop(scene, "scene_amplitud", text="Amplitud")
            col.prop(scene, "scene_eje", text="Eje de oscilación")
        
        layout.separator()
        row = layout.row() # Crea una fila
        
        # Añade el botón que ejecuta el operador. Haciendo referencia al operaodor "bpy.ops.object.gen_ciudad"
        row.operator("object.gen_car", text=f"Crear Coche {metodo_texto}")
        row.operator("object.delete_cars", text="Borrar Coches")
        
        layout.separator()

def register():
    bpy.utils.register_class(ProceduralCityPanel) # Registra la clase del panel
    bpy.utils.register_class(CarGenerator) # Registra la clase del panel
    
    """
    
    Propiedades de la escena
    
    """
                                    
    # Registrar las propiedades
    bpy.types.Scene.n_calles_x = bpy.props.IntProperty(name="n_calles_x", min=1, default=10)
    bpy.types.Scene.n_calles_y = bpy.props.IntProperty(name="n_calles_y", min=1, default=10)
    bpy.types.Scene.ancho_calles = bpy.props.FloatProperty(name="Ancho Calle", min=1, default=10)
    bpy.types.Scene.tam_manzana = bpy.props.FloatProperty(name="Tamaño manzana", min=0.5, default=5)
    bpy.types.Scene.alt_edif_min = bpy.props.FloatProperty(name="Altura Minima", min=1, default=20)
    bpy.types.Scene.alt_edif_max = bpy.props.FloatProperty(name="Altura Maxima", min=2, default=70)
    bpy.types.Scene.car_velocity = bpy.props.FloatProperty(name="Velocidad del coche", min=1, default=1)
    bpy.types.Scene.car_scale = bpy.props.IntProperty(name="Escala del coche", min=5, max=10, default=5) # Comprobar si 10 es suficiente
    bpy.types.Scene.car_height = bpy.props.IntProperty(name="Altura del coche", min=20, default=50) # Comprobar si 10 es suficiente
    
    # Se crea y registra la propiedad de enumeracion, con su nombre, su lista de itemas, descripción y valor por defecto
    bpy.types.Scene.scene_metodo = bpy.props.EnumProperty(
        name="scene_metodo",
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
    bpy.types.Scene.scene_velocidad = bpy.props.FloatVectorProperty(name="scene_velocidad", description='Vector velocidades de Hermite', default=(0.0, 0.0, 0.0), min=-10.0, max=10.0, size=3)
    # Registra la propiedad de tensión
    bpy.types.Scene.scene_tension = bpy.props.FloatProperty(name="scene_tension", description="Tensión para Catmull-Rom", default=2, min=0.0, max=10.0)
    
    bpy.types.Scene.scene_amplitud = bpy.props.FloatProperty(name="scene_amplitud", description="Amplitud de la oscilación", min=0.1, default = 1)
    bpy.types.Scene.scene_frecuencia = bpy.props.FloatProperty(name="scene_frecuencia", description="Frecuencia de la oscilación", min=0.1, default = 1)
    bpy.types.Scene.scene_oscilacion = bpy.props.BoolProperty(name='scene_oscilacion', description='Permite aplicar oscilación', default=False)
    bpy.types.Scene.scene_eje = bpy.props.EnumProperty(name="scene_eje", description="Selecciona una interpolación",
                                                  items=[
                                                      ('EX', "Eje X", "Oscila sobre el eje x"),
                                                      ('EY', "Eje Y", "Oscila sobre el eje y"),
                                                      ('EZ', "Eje Z", "Oscila sobre el eje z")],
                                                    default='EX',  # Valor por defecto
                                                )
    bpy.types.Scene.ncoches = bpy.props.IntProperty(name="ncoches", description="Número de coches creados en la escena", min=0, max=50, default=1)
    
    """
    
    Propiedades del objeto
    
    """
    
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
    
    bpy.types.Object.amplitud = bpy.props.FloatProperty(name="amplitud", description="Amplitud de la oscilación", min=0.1, default = 1)
    bpy.types.Object.frecuencia = bpy.props.FloatProperty(name="frecuencia", description="Frecuencia de la oscilación", min=0.1, default = 1)
    bpy.types.Object.oscilacion = bpy.props.BoolProperty(name='oscilacion', description='Permite aplicar oscilación', default=False)
    bpy.types.Object.eje = bpy.props.EnumProperty(name="eje", description="Selecciona una interpolación",
                                                  items=[
                                                      ('EX', "Eje X", "Oscila sobre el eje x"),
                                                      ('EY', "Eje Y", "Oscila sobre el eje y"),
                                                      ('EZ', "Eje Z", "Oscila sobre el eje z")],
                                                    default='EX',  # Valor por defecto
                                                )

def unregister():
    bpy.utils.unregister_class(ProceduralCityPanel) # Elimina del registro la clase del panel
    bpy.utils.unregister_class(CarGenerator) # Elimina del registro la clase del panel
    
    # Eliminar las propiedades de la escena
    del bpy.types.Scene.n_calles_x
    del bpy.types.Scene.n_calles_y
    del bpy.types.Scene.ancho_calles
    del bpy.types.Scene.tam_manzana
    del bpy.types.Scene.alt_edif_min
    del bpy.types.Scene.alt_edif_max
    del bpy.types.Scene.car_velocity
    del bpy.types.Scene.car_scale
    del bpy.types.Scene.ncoches
    del bpy.types.Scene.scene_metodo 
    del bpy.types.Scene.scene_velocidad 
    del bpy.types.Scene.scene_tension
    
    del bpy.types.Scene.scene_frecuencia
    del bpy.types.Scene.scene_amplitud
    del bpy.types.Scene.scene_oscilacion
    del bpy.types.Scene.scene_eje
    
    # Eliminar las propiedades del objeto
    del bpy.types.Object.metodo 
    del bpy.types.Object.velocidad
    del bpy.types.Object.tension
    del bpy.types.Object.keyframe
    
    del bpy.types.Object.frecuencia
    del bpy.types.Object.amplitud
    del bpy.types.Object.oscilacion
    del bpy.types.Object.eje

if __name__ == "__main__": # Si el script es ejecutado directamente se llama a la función register.
    register()