import bpy #type: ignore
import math

def get_posicion_y_loop(frm: float, radio: float, vel: int):
    """ Return object location for frame 'frm'
    
    If time <= 0, pos.y = 0
    If time > 0, pos.y = sin(vt)*r
    """
    
    # each frame is 1/24 secs. First, we compute time
    t = frm/24.0
    
    if t <= 0 :
        # at the start the position of the object is 0.0 (initial position)
        posy = 0.0
    elif t > 0 :
        # using polar coordinates it controls de position using the sine of the angular velocity       
        posy = math.sin(vel*t)*radio
        
    return posy


# registers the function in order to use it as driver in Blender
bpy.app.driver_namespace['get_pos_y'] = get_posicion_y_loop