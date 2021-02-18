from facade import FacademakerFacade
from front_end_set import TriangleSet, SquareSet, PyramidSet, DiamondSet, QuadGroupSet
from facade_link_info import FUNCTION_TYPES, FUNCTION_SHIFT_VALUES

def facade_from_dict(data_dict, x_spacing=None, z_spacing=1000., y_delta=500., other_parameters=None):
    """function that returns a FacademakerObject based on a front-end data dict
    input:
    x_spacing: float (None)         - overwriting the x_spacing value, if None using the default one
    z_spacing: float (1000.)        - setting the z_spacing of the cassette
    y_delta:   float (500.)         - setting the maximum thickness of the cassette
    other_parameters: dict (None)   - parameter dicts, uses the default values if none given
    return:
    FacademakerFacade object"""

    try:
        data_dict["hc"]=data_dict["hc_rel"]*y_delta
    except:
        print("no hc_rel defined")

    # non relative assignment of the x_spacing, default is based on 'frat'
    if x_spacing is None:
        data_dict["x_spacing"]=z_spacing*data_dict['frat']
    else:
        data_dict["x_spacing"]=x_spacing
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

    f.set_selection_pattern(data_dict["ftypo"])

    if other_parameters is None:
        print("facade_from_dict other_parameters is None")
    else:
        print("facade_from_dict has other_parameters")
        print(other_parameters)

    FUNCTION_MAP[FUNCTION_TYPES[data_dict['ft']]](f, other_parameters, data_dict)

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

def triangle_function(facade, o_p, data_dict):
    """function to parse triangles with"""
    f_b_set=TriangleSet(
        x=data_dict["x_spacing"],
        y=data_dict["z_spacing"],
        hs=data_dict["mapped_hs"],
        s=FUNCTION_SHIFT_VALUES[data_dict['ft']]
    )

    facade.objects_per_tile=2
    apply_all_transformations(f_b_set, data_dict)
    
    if data_dict["base_objects"]!=2:
        facade.set_multi_triangles(
            f_b_set.flat_clone(),
            other_parameters=o_p,
            obj_idx=2)

    facade.set_multi_triangles(
        ptsss=f_b_set.generate(),
        other_parameters=o_p
    )

def square_function(facade, o_p, data_dict):
    """function to parse squares with"""
    f_b_set=SquareSet(
        x=data_dict["x_spacing"],
        y=data_dict["z_spacing"],
        hs=data_dict["mapped_hs"],
        s=FUNCTION_SHIFT_VALUES[data_dict['ft']]
    )

    f_b_2=SquareSet(
        x=data_dict["x_spacing"],
        y=data_dict["z_spacing"],
        hs=data_dict["mapped_hs"],
        s=FUNCTION_SHIFT_VALUES[data_dict['ft']]
    )

    apply_all_transformations(f_b_set, data_dict)

    if data_dict["base_objects"]!=2:
        facade.set_multi_squares(
            f_b_2.flat_clone(),
            other_parameters=o_p,
            obj_idx=2
        )
    
    ptsss=f_b_set.generate()
    fold_idxs=f_b_set.fold_idxs()

    facade.set_multi_squares(
        ptsss=ptsss,
        other_parameters=o_p, 
        fold_idxs=fold_idxs
    )

def diamond_function(facade, o_p, data_dict):
    """function to parse diamonds with"""

    f_b_set=DiamondSet(
        x=data_dict["x_spacing"],
        y=data_dict["z_spacing"],
        hs=data_dict["mapped_hs"],
    )

    apply_all_transformations(f_b_set, data_dict)

    if data_dict["base_objects"]!=2:
        facade.set_multi_squares(
            f_b_set.flat_clone(),
            other_parameters=o_p,
            obj_idx=2
        )
    
    ptsss=f_b_set.generate()
    fold_idxs=f_b_set.fold_idxs()

    facade.set_multi_squares(
        ptsss=ptsss,
        other_parameters=o_p, 
        fold_idxs=fold_idxs
    )
    
def pyramid_function(facade, o_p, data_dict):
    """function to parse pyramids with"""

    f_b_set=PyramidSet(
        x=data_dict["x_spacing"],
        y=data_dict["z_spacing"],
        hs=data_dict["mapped_hs"],
        a=data_dict["a"],
        b=data_dict["b"],
        hc=data_dict["hc"],
        s=FUNCTION_SHIFT_VALUES[data_dict['ft']]
    )

    apply_all_transformations(f_b_set, data_dict)

    if data_dict["base_objects"]!=2:
        facade.set_multi_squares(
            f_b_set.flat_clone(),
            other_parameters=o_p,
            obj_idx=2
        )
    
    ptsss=f_b_set.generate()
    c_ptss=f_b_set.get_c_ptss()

    facade.set_multi_pyramids(
        ptsss=ptsss,
        c_ptss=c_ptss,
        other_parameters=o_p
    )

def quad_group_function(facade, o_p, data_dict):
    """function to parse quad_group with"""

    f_b_set=QuadGroupSet(
        x=data_dict["x_spacing"],
        y=data_dict["z_spacing"],
        hs=data_dict["mapped_hs"],
        a=data_dict["a"],
        b=data_dict["b"],
        s=FUNCTION_SHIFT_VALUES[data_dict['ft']]
    )

    f_b_2=SquareSet(
        x=data_dict["x_spacing"],
        y=data_dict["z_spacing"],
        hs=data_dict["mapped_hs"],
        s=FUNCTION_SHIFT_VALUES[data_dict['ft']]
    )

    apply_all_transformations(f_b_set, data_dict)
    # apply_all_transformations(f_b_2, data_dict)

    if data_dict["base_objects"]!=2:
        facade.set_multi_squares(
            f_b_2.flat_clone(),
            other_parameters=o_p,
            obj_idx=2
        )
    
    ptssss=f_b_set.generate()

    facade.set_multi_quad_blocks(
        ptssss=ptssss,
        other_parameters=o_p
    )

FUNCTION_MAP={
    'triangle':   triangle_function,
    'square':     square_function,
    'diamond':    diamond_function,
    'pyramid':    pyramid_function,
    'quad_group': quad_group_function,
}