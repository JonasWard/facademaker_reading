from facade import FacademakerFacade
from front_end_set import TriangleSet, SquareSet, DiamondSet
from facade_link_info import FUNCTION_TYPES, FUNCTION_SHIFT_VALUES

def facade_from_dict(data_dict, z_spacing=1000., y_delta=500.):
    """function that returns a FacademakerObject based on a front-end data dict"""

    data_dict["x_spacing"]=z_spacing*data_dict['frat']
    data_dict["z_spacing"]=z_spacing
    data_dict["y_delta"]=y_delta
    data_dict["mapped_hs"]=[h*data_dict["y_delta"] for h in data_dict["hs"]]

    global FUNCTION_MAP, FUNCTION_TYPES
    f=FacademakerFacade(
        x_count=data_dict['fgh'],
        x_spacing=data_dict["x_spacing"],
        z_count=data_dict['fgv'],
        z_spacing=data_dict["z_spacing"]
    )

    FUNCTION_MAP[FUNCTION_TYPES[data_dict['ft']]](f, data_dict)

    return f

def apply_all_transformations(f_b_set, data_dict):
    if data_dict["mirrh"]:
        f_b_set.h_mir()
    if data_dict["mirrv"]:
        f_b_set.v_mir()
    if data_dict["konh"]:
        f_b_set.h_kon()
    if data_dict["konv"]:
        f_b_set.v_kon()
    f_b_set.h_rot(data_dict["roth"])
    f_b_set.v_rot(data_dict["rotv"])

def triangle_function(facade, data_dict):
    """function to parse triangles with"""
    f_b_set=TriangleSet(
        x=data_dict["x_spacing"],
        y=data_dict["z_spacing"],
        hs=data_dict["mapped_hs"],
        s=FUNCTION_SHIFT_VALUES[data_dict['ft']]
    )

    facade.objects_per_tile=2
    apply_all_transformations(f_b_set, data_dict)
    
    facade.set_multi_triangles(f_b_set.generate())

def square_function(facade, data_dict):
    """function to parse squares with"""
    f_b_set=SquareSet(
        x=data_dict["x_spacing"],
        y=data_dict["z_spacing"],
        hs=data_dict["mapped_hs"],
        s=FUNCTION_SHIFT_VALUES[data_dict['ft']]
    )

    apply_all_transformations(f_b_set, data_dict)
    
    facade.set_multi_squares(f_b_set.generate())
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