# import Rhino.Geometry as rg
from triangle_data import TriangleData
from square_data import SquareData

def create_mns(m, n, shift = 0):
    mns_obj = {'m': m,'n': n,'s': shift}
    for j in range(n):
        row = []
        for i in range(m):
            row.append(j * m + i)
        mns_obj[j] = row
        
    return mns_obj

default_base_parameters = {
    "x_cnt" : 5,
    "z_cnt" : 5,
    "x_dim" : 1.0,
    "z_dim" : 1.0,
    'h'     : .1
}

f_dict = {
    "q1"     : {"mns_single": create_mns(1,1), "mns_complex": create_mns(1,1), "pt_cnt": 4, "has_center": False, "co_planar": True},
    "q1lift" : {"mns_single": create_mns(1,1), "mns_complex": create_mns(2,2), "pt_cnt": 4, "has_center": False, "co_planar": True},
    "q4"     : {"mns_single": create_mns(2,2), "mns_complex": create_mns(4,4), "pt_cnt": 4, "has_center": False, "co_planar": True},
    "d2"     : {"mns_single": create_mns(1,1), "mns_complex": create_mns(2,2), "pt_cnt": 4, "has_center": False, "co_planar": False},
    "d4"     : {"mns_single": create_mns(1,1), "mns_complex": create_mns(2,2), "pt_cnt": 4, "has_center": True , "co_planar": False}
}

def has_a_center(data_dict):
    try:
        data_dict["mid"]
        return True
    except:
        return False

def has_multiple_types(data_dict):
    value = 0
    for special_tag in ["roth", "rotv", "mirrh", "mirrv", "konh", "konv"]:
        value += data_dict[special_tag]

    if value > 0:
        return True
    else:
        return False

def mns_gen(data_dict):
    global f_dict

    data_dict["mapping"] = f_dict[data_dict["ft"]]["mns_single"]
    
    if has_multiple_types:
        data_dict["mns"] = f_dict[data_dict["ft"]]["mns_complex"]
    else:
        data_dict["mns"] = f_dict[data_dict["ft"]]["mns_single"]

    return data_dict

def extend_data_dict(data_dict):
    global f_dict

    data_dict["has_center"] = f_dict[data_dict["ft"]]["has_center"]
    if data_dict["has_center"]:
        data_dict = set_abh_mid(data_dict)

    data_dict["pt_cnt"] = f_dict[data_dict["ft"]]["pt_cnt"]
    data_dict = mns_gen(data_dict)
    data_dict["co_planar"] = f_dict[data_dict["ft"]]["co_planar"]

    return data_dict

def set_abh_mid(data_dict):
    try:
        a,b,h = data_dict["mid"]
    except:
        print("no mid point found while expected")
        a,b,h = .5, .5, .1
    
    data_dict['a'] = a
    data_dict['b'] = b
    data_dict['h'] = h

    return data_dict

def top_height_setting(data_dict, base_parameters):
    data_dict["h_a"] = data_dict['h'] * base_parameters['h'] + min(data_dict["hs"])
    data_dict["h_b"] = data_dict['h'] * base_parameters['h'] + min(data_dict["hs"])

    return data_dict

def set_heights(data_dict, base_parameters = None, minimum_height = .2):
    print("setting the heights")
    if base_parameters is None:
        global default_base_parameters
        base_parameters = default_base_parameters

    xy_dim = base_parameters["z_dim"]

    data_dict["xy_dim"] = xy_dim

    # checking if an adequate amount of heights are available, if not adding
    hs = [ h * xy_dim for h in data_dict["hs"] ]
    if len(hs) == data_dict["pt_cnt"]:
        pass
    elif len(hs) == 1:
        print("having to add extra data points, Required: {}, give: {}".format(data_dict["pt_cnt"], len(data_dict["hs"]) ) )
        hs = [ hs[0] for i in range( data_dict["pt_cnt"] ) ]
    else:
        hs += [ minimum_height for i in range( data_dict["pt_cnt"] - len( data_dict["hs"]) ) ]

    data_dict["hs"] = hs

    # checking whether the structure is compliant with the minimum height
    h_offset = 0
    if data_dict["has_center"]:
        data_dict = top_height_setting(data_dict, base_parameters)

        h_min = min( [data_dict["h_a"], data_dict["h_b"] ])
        if h_min < 0:
            h_offset = abs(h_min)

    hs_min = min(hs)
    h_offset = h_offset if (hs_min + h_offset > minimum_height) else hs_min

    if data_dict["has_center"]:
        data_dict["h_a"] += h_offset
        data_dict["h_b"] += h_offset

    data_dict["hs"] = [ h + h_offset for h in hs ]

    return data_dict

def gen_objects(data_dict):
    base_object = None
    if data_dict["pt_cnt"] == 3:
        base_object = TriangleData(
            l = data_dict["xy_dim"]*data_dict["frat"],
            w = data_dict["xy_dim"],
            hs = data_dict["hs"]
        )
    elif data_dict["pt_cnt"] == 4:
        base_object = SquareData(
            l = data_dict["xy_dim"]*data_dict["frat"],
            w = data_dict["xy_dim"],
            hs = data_dict["hs"]
        )

    base_set = []
    mns = data_dict["mns"]
    m, n = mns['m'], mns['n']

    for i in range(m):
        row = []
        for j in range(n):
            loc_obj = base_object.clone()

            if (data_dict["rmd"][i][j]["flip_h"]):
                loc_obj.flip_h()

            if (data_dict["rmd"][i][j]["flip_v"]):
                loc_obj.flip_v()

            if (data_dict["rmd"][i][j]["inside"]):
                loc_obj.flip_in_out()

            loc_obj.rotate(data_dict["rmd"][i][j]["rotation"])

            row.append(loc_obj)
        base_set.append(row)

    data_dict["object_set"] = base_set

    return data_dict

def rot_ref_dir(data_dict):
    m, n = data_dict["mns"]['m'], data_dict["mns"]['n']

    rot_v = 0
    flip_v = 0
    inside_v = 0

    values = []

    for j in range(n): # through each row

        rot_h = 0
        flip_h = 0
        inside_h = 0
        
        row_values = []
        
        for i in range(m): # through each column
            
            row_values.append({
                "flip_h": bool (flip_h % 2),
                "flip_v": bool (flip_v % 2),
                "inside": bool ( (inside_v + inside_h) % 2),
                "rotation": (rot_h + rot_v) % 4
            })
            
            rot_h += data_dict["roth"]
            flip_h += data_dict["mirrh"]
            inside_h += data_dict["konh"]

        values.append(row_values)

        rot_v += data_dict["rotv"]
        flip_v += data_dict["mirrv"]
        inside_v += data_dict["konv"]

    data_dict["rmd"] = values

    return data_dict

def initialize_points(data_dict, base_parameters = None, minimum_height = .2):
    data_dict = extend_data_dict(data_dict)
    data_dict = set_heights(data_dict, base_parameters, minimum_height)
    data_dict = rot_ref_dir(data_dict)
    data_dict = gen_objects(data_dict)

    return data_dict
