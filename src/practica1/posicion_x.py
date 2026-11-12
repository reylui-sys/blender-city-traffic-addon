import bpy #type: ignore
import math

def get_posicion_x_loop(frm: float, radio: float, vel: int):
    """ Return object location for frame 'frm'
    
    If time < 0, pos.x = radio
    If time > 5, pos.x = r*cos(w)
    In between, linear interpolation
    """
    
    # each frame is 1/24 secs. First, we compute time
    t = frm/24.0
    
    if t <= 0 :
        # at the start the position of the object is the radius (initial position)
        posx = radio
    elif t > 0 :
        # using polar coordinates it controls de position using the cosine of the angular velocity
        posx = math.cos(vel*t)*radio

    return posx

# registers the function in order to use it as driver in Blender
bpy.app.driver_namespace['get_pos_x'] = get_posicion_x_loop