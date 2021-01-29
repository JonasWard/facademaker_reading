import type_generation
from read_link import string_reader

def height_mapping(c00, c01, c10, c11):
    return c00, c10, c11, c01   # h0, h1, h2, h3 (counter clockwise from bottom left)

def side_detection_lifted(heights):
    # heights presumed ordered (h0, h1, h2, h3)
    h0, h1 = min(heights), max(heights)
    print("h0: {}, h1: {}".format(h0, h1) )
    idxs = []
    for i, h in range(heights):
        if h == h1:
            idxs.append(i)
    
    idxs = idxs.sort()
    if ( idxs[0] + 1 == idxs[1] ):
        return idxs[0], h0, h1
    else:
        return idxs[1], h0, h1

def is_complex(d_d):
    return not(not(d_d["mirrh"]) and not(d_d["mirrv"]) and not(d_d["konh"]) and not(d_d["konv"]) and d_d["roth"] == 0 and d_d["rotv"] == 0)

def height_flipping(hs, bot_rot = 0, right_rot = 0, bot_flip = False, right_flip = False)

def check_reflections_double(d_d, h0, h1, side):
    print("double reflections check")
    hs = [h0, h1]

    if not(is_complex(d_d) ):
        print("no reflections to consider, is not complex")
        return False, [hs, side]  # is complex, parameters

    else:
        print("reflections and rotations to consider, I am complex")
        p_list = [ [ [ hs[:], side ] for i in range(2)] for i in range(2) ]

        return True, p_list

def check_reflections_quad(d_d, h0, h1, h2, h3, a, b):
    print("quad reflections check")
    hs = [h0, h1, h2, h3]
    ab = [a, b]

    if not(is_complex(d_d) ):
        print("no reflections to consider, is not complex")
        return False, [hs, ab]  # is complex, parameters

    else:
        print("reflections and rotations to consider, I am complex")
        p_list = [ [ [ hs[:], ab[:] ] for i in range(2)] for i in range(2) ]

        return True, p_list   # is complex, parameters

def string_to_pointsets(d_d, xy_dimension = 750, z_dimension = 100, def_h = .2):
    pts, shp, rshift, xres, yres = "pts", "shp", "rshift", "xres", "yres"
    
    try:
        frat = d_d["frat"]
        l, w = xy_dimension * frat, xy_dimension
        print("w x l values set as: {} x {}".format(w, l) )
    except:
        l, w = xy_dimension, xy_dimension
        print("no tag_frat defined, w x l values set as: {} x {}".format(w, l))

    try:
        hs = height_mapping( d_d["c00"], d_d["c01"], d_d["c10"], d_d["c11"] )
        h0, h1, h2, h3 = [h * z_dimension for h in hs]
        print("coordinate heights: {}, {}, {}, {}".format(h0, h1, h2, h3) )
    except:
        h0, h1, h2, h3 = [def_h * z_dimension for i in range(4)]
        print("not all heights defined, all heights assigned as relative .2 : {}, {}, {}, {}".format(h0, h1, h2, h3) )

    try:
        a, b, h5 = d_d["mid"]
        if h5 is None:
            h5 = z_dimension * def_h
        print("midpoint values: a: {}, b: {}, h: {}".format(a, b, h5) )
    except:
        a, b, h5 = .5, .5, z_dimension * def_h
        print("no mid_tag, midpoint values set as: a: {}, b: {}, h: {}".format(a, b, h5) )

    output_dict = {pts : [], shp : (2, 2), rshift : 0, xres : 5, yres : 6}

    try:
        if d_d["ft"] == "q1":
            h = h0
            print("function: single value square")
            output_dict[shp] = (1, 1)
            output_dict[pts] = [type_generation.simple_square(l, w, h) ]
        elif d_d["ft"] == "q1lift":
            print("function: two values side lift")
            side_value, h0, h1 = side_detection_lifted( [h0, h1, h2, h3] )
            print("active side {}, h0: {}, h1: {}".format(side_value, h0, h1))
        elif d_d["ft"] == "q4":
            if is_complex:
                pass
            else:
                output_dict[pts].extend(type_generation.simple_square(l, w, a, b, h0, h1, h2, h3) )
        elif d_d["ft"] == "d2":
            print("function: all sides lifted")
        elif d_d["ft"] == "d4":
            print("function: square with lifted centerpoint")
    except:
        print("no function defined")

if __name__ == "__main__":
    f = open("links.csv", 'r')

    for string in f.readlines():
        print("========= start reading =========")
        data_dict = string_reader(string)
        print("========= start generating =========")
        print( string_to_pointsets(data_dict) ) 