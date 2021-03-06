from base_conversions import baseconvert

def clean_string(string):
    parts = string.split('/')
    part = parts[-1]

    part = part.replace('?', '')
    part = part.replace("index.php", '')
    segments = part.split('&')

    return segments

def string_to_dict(string):
    loc_dict = {}
    for seg in clean_string(string):
        a, b = seg.split('=')
        loc_dict[a] = b

    return loc_dict

def complete_tag_list(string):
    tag_list = []
    for seg in clean_string(string):
        a, b = seg.split('=')
        tag_list.append(a)

    return tag_list

def ftypo_handling(data_dict):
    found_key = False
    for key in data_dict.keys():
        if "ftypo" in key:
            found_key = True
            ftypo = data_dict[key]
            break
    
    if not(found_key):
        print("no ftypo found, populated with all int 1")
        row = [ 1 for i in range( data_dict["fgh"] ) ]
        data_dict["ftypo"] = [ row[:] for i in range( data_dict["fgv"] ) ]
    
    else:
        if key == "ftypo":
            ftypo = str( bin (int (data_dict["ftypo"], 32 ) ) )[2:]
            ftypo = [ftypo[i * data_dict["fgh"] : (i + 1) * data_dict["fgh"]] for i in range(data_dict["fgv"])]
            ftypo = [ [int(c) for c in chars] for chars in ftypo]

        else:
            key_remainder = int(key.replace("ftypo", '') )
            ftypo = data_dict[key].split('_')
            ftypo = [baseconvert(int(chars, 36), 2 ** key_remainder) for chars in ftypo]
            ftypo = [ [int(c) for c in str(number)] for number in ftypo]

    data_dict["ftypo"] = ftypo

    return data_dict

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

    try:
        coords = loc_dict["mid"].split("%2C")
        coords = [c.replace('\n', '') for c in coords]
        for i, c in enumerate(coords):
            if c is None or c == '':
                coords[i] = None
            else:
                coords[i] = float(c)
        loc_dict["mid"] = coords
    except:
        print("no mid tag present")

    hs = []
    for h_tag in ["c00", "c01", "c10", "c11"]:
        try:
            hs.append(loc_dict[h_tag])
        except:
            print("no tag {} found in this data_dict".format(h_tag))

    loc_dict["hs"] = hs

    loc_dict = ftypo_handling(loc_dict)

    return loc_dict

if __name__ == "__main__":
    string = "https://facademaker.alucobond.com/?ft=d2&fp=0&fgv=5&fgh=7&frat=1.3953488372093024&ftypo=tvvvvvv&mirrh=0&mirrv=0&roth=0&rotv=0&konh=0&konv=0&mat=&c00=1&c01=0&c10=0&c11=0.7"
    print(string_reader(string))