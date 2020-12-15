import type_generation
from read_link import string_to_dict

def height_mapping(c00, c01, c10, c11):
    return c00, c10, c11, c01   # h0, h1, h2, h3 (counter clockwise from bottom left)

def string_to_pointsets(string, xy_dimension = 750, z_dimension = 100):
    this_dict = string_to_dict(string)

    try:
        frat = this_dict["frat"]
    except:
        print("no tag_frat defined, default 1.0 assigned")
        frat = 1.0

    try:
        h0, h1, h2, h3 = height_mapping(this_dict["c00"], this_dict["c01"], this_dict["c10"], this_dict["c11"])
    except:
        print("not all heights defined, all heights assigned as relative .2")
        h0, h1, h2, h3 = .2, .2, .2, .2

    w, l = xy_dimension * frat, xy_dimension

    try:
        if this_dict["ft"] == 'q1':
            pass
    except:
        print("no function defined")
