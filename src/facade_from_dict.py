from facade import FacademakerFacade
from facade_link_info import FUNCTION_TYPES

def facade_from_dict(data_dict, z_spacing=1000.):
    """function that returns a FacademakerObject based on a front-end data dict"""

    data_dict["x_spacing"]=z_spacing*data_dict['frat']
    data_dict["z_spacing"]=z_spacing

    global FUNCTION_MAP, FUNCTION_TYPES
    f=FacademakerFacade(
        x_count=data_dict['fgh'],
        x_spacing=data_dict["x_spacing"],
        z_count=data_dict['fgv'],
        z_spacing=data_dict["z_spacing"]
    )

    FUNCTION_MAP[FUNCTION_TYPES[data_dict['ft']]](f, data_dict)

    return f

def triangle_function(facade, data_dict):
    """function to parse triangles with"""
    print("parsing triangle")
    pass

def square_function(facade, data_dict):
    """function to parse squares with"""
    print("parsing squares")
    pass

def diamond_function(facade, data_dict):
    """function to parse diamonds with"""
    print("parsing diamonds not yet implemented!")
    pass

def pyramid_function(facade, data_dict):
    """function to parse pyramids with"""
    print("parsing pyramids")
    pass

def quad_group_function(facade, data_dict):
    """function to parse quad_group with"""
    print("parsing quad_group")
    pass

FUNCTION_MAP={
    'triangle':   triangle_function,
    'square':     square_function,
    'diamond':    diamond_function,
    'pyramid':    pyramid_function,
    'quad_group': quad_group_function,
}