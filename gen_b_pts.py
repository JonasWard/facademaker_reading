# import Rhino.Geometry as rg

def create_mns(m, n, shift = 0):
    mns_obj = {'m': m,'n': n,'s': shift}
    for j in range(n):
        row = []
        for i in range(m):
            row.append(j * m + i)
        mns_obj[j] = row
        
    return mns_obj

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
    
    if has_multiple_types:
        return f_dict[data_dict["ft"]]["mns_complex"]
    else:
        return f_dict[data_dict["ft"]]["mns_single"]

def extend_data_dict(data_dict):
    global f_dict

    if f_dict[data_dict["ft"]]["has_center"]:
        data_dict = set_abh_mid(data_dict)

    data_dict["msn"] = mns_gen(data_dict)
    data_dict["mapping"] = f_dict[data_dict["ft"]]["mns_single"]
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

def set_heights(data_dict, minimum_height):
    pass

def initialize_points(data_dict, base_parameters, minimum_height = .2):
    data_dict = extend_data_dict(data_dict)

    # data_dict["hs"] = 

    return data_dict
