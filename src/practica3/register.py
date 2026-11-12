import bpy #type: ignore

def register():
    bpy.types.Scene.tam_manzana = bpy.props.FloatProperty(min = 0.5, default = 0.5)
    bpy.types.Scene.ancho_calles = bpy.props.FloatProperty(min = 1, default = 1)
    bpy.types.Scene.alt_edif_max = bpy.props.FloatProperty(min = 2, default = 5)
    bpy.types.Scene.alt_edif_min = bpy.props.FloatProperty(min = 1, default = 1)
    bpy.types.Scene.alt_edif = bpy.props.FloatProperty(min = 2, default = 5)
    bpy.types.Scene.n_calles_x = bpy.props.IntProperty(min = 1, default = 10)
    bpy.types.Scene.n_calles_y = bpy.props.IntProperty(min = 1, default = 10)
    bpy.types.Scene.prob_edificio = bpy.props.FloatProperty(min = 0, max = 1, default = 1)
    
def unregister():
    del bpy.types.Scene.tam_manzana
    del bpy.types.Scene.ancho_calles
    del bpy.types.Scene.alt_edif_max
    del bpy.types.Scene.alt_edif_min
    del bpy.types.Scene.n_calles_x
    del bpy.types.Scene.n_calles_y
    del bpy.types.Scene.prob_edificio