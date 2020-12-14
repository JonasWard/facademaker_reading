def string_to_dict(string):

    parts = string.split('/')
    part = parts[-1]

    # print(part)
    part = part.replace('?', '')
    segments = part.split('&')
    # print(segments)
    loc_dict = {}
    for seg in segments:
        a, b = seg.split('=')
        loc_dict[a] = b

    return loc_dict

def string_reader(string):

    loc_dict = string_to_dict(string)

    for boolean_tag in ["mirrh", "mirrv", "konh", "konv"]:
        try:
            loc_dict[boolean_tag] = bool(loc_dict[boolean_tag])
        except:
            try:
                print("wrong boolean_tag {} : {}".format(boolean_tag, loc_dict[boolean_tag] ) )
            except:
                print("non present boolean_tag {}".format(boolean_tag) )

    for integer_tag in ["fgv", "fgh", "fp", "roth", "rotv"]:
        try:
            loc_dict[integer_tag] = int(loc_dict[integer_tag])
        except:
            try:
                print("wrong integer_tag {} : {}".format(integer_tag, loc_dict[integer_tag] ) )
            except:
                print("non present integer_tag {}".format(integer_tag) )

    for float_tag in ["frat", "c00", "c01", "c10", "c11"]:
        try:
            loc_dict[float_tag] = float(loc_dict[float_tag])
        except:
            try:
                print("wrong float_tag {} : {}".format(float_tag, loc_dict[float_tag] ) )
            except:
                print("non present float_tag {}".format(float_tag) )

    loc_dict["ftypo"] = bin(int(loc_dict["ftypo"], 32))

    return loc_dict

if __name__ == "__main__":
    string = "https://facademaker.alucobond.com/?ft=d2&fp=0&fgv=5&fgh=7&frat=1.3953488372093024&ftypo=tvvvvvv&mirrh=0&mirrv=0&roth=0&rotv=0&konh=0&konv=0&mat=&c00=1&c01=0&c10=0&c11=0.7"
    print(string_reader(string))