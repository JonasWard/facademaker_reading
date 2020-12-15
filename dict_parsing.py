import type_generation
from read_link import string_reader

def height_mapping(c00, c01, c10, c11):
    return c00, c10, c11, c01   # h0, h1, h2, h3 (counter clockwise from bottom left)

def string_to_pointsets(string, xy_dimension = 750, z_dimension = 100):
    this_dict = string_reader(string)
    print(this_dict)

    try:
        frat = this_dict["frat"]
        w, l = xy_dimension * frat, xy_dimension
        print("relative values set as: {} x {}".format(w, l) )
    except:
        w, l = xy_dimension, xy_dimension
        print("no tag_frat defined, relative values set as: {} x {}".format(w, l))

    try:
        hs = height_mapping( this_dict["c00"], this_dict["c01"], this_dict["c10"], this_dict["c11"] )
        h0, h1, h2, h3 = [h * z_dimension for h in hs]
        print("relative coordinate heights: {}, {}, {}, {}".format(h0, h1, h2, h3) )
    except:
        h0, h1, h2, h3 = [.2 * z_dimension for i in range(4)]
        print("not all heights defined, all heights assigned as relative .2")

    try:
        if this_dict["ft"] == "q1":
            print("funtion: single value square")
        elif this_dict["ft"] == "q1lift":
            print("funtion: two values side lift")
        elif this_dict["ft"] == "q4":
            print("funtion: four flat squares")
        elif this_dict["ft"] == "d2":
            print("funtion: all sides lifted")
        elif this_dict["ft"] == "d4":
            print("funtion: square with lifted centerpoint")
    except:
        print("no function defined")

if __name__ == "__main__":
    string = "https://facademaker.alucobond.com/?ft=d2&fp=0&fgv=5&fgh=7&frat=1.3953488372093024&ftypo=tvvvvvv&mirrh=0&mirrv=0&roth=0&rotv=0&konh=0&konv=0&mat=&c00=1&c01=0&c10=0&c11=0.7"
    print(string_to_pointsets(string))