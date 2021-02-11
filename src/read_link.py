def baseconvert(n, base):
    """function that converts positive decimal integer n to equivalent into
    another give base (2-36)"""

    digits="0123456789abcdefghijklmnopqrstuvwxyz"

    try:
        n=int(n)
        base=int(base)
    except:
        return ""

    if (n<0) or (base<2) or (base>36):
        return ""

    s=""

    while 1:
        r=n%base
        s=digits[r]+s
        n-=r
        n=int(n/base)
        if n==0:
            break

    return s
    
def clean_string(string):
    """funnction that cleans ans plits the link string in different segments"""
    parts=string.split('/')
    part=parts[-1]

    part=part.replace('?', '')
    part=part.replace("index.php", '')
    segments=part.split('&')

    return segments

def string_to_dict(string):
    """function that turns the string into a dict"""
    loc_dict = {}
    for seg in clean_string(string):
        a, b = seg.split('=')
        loc_dict[a] = b

    return loc_dict

# def complete_tag_list(string):
#     tag_list = []
#     for seg in clean_string(string):
#         a, b = seg.split('=')
#         tag_list.append(a)

#     return tag_list

def ftypo_handling(data_dict):
    """function that sets the ftypo key. In case there is an ftypo2 or an ftypo3,
    a base 36 is assumed otherwise 32, as well as the amount of base object
    types (2, 4, 8). Afterwards the values are sliced into nested lists, similar
    to the building facade n.m position matrix"""
    found_key=False
    for key in data_dict.keys():
        if "ftypo" in key:
            found_key=True
            ftypo=data_dict[key]
            break
    
    if not(found_key):
        data_dict["base_objects"]=2
        print("no ftypo found, populated with all int 1")
        row=[ 1 for i in range( data_dict["fgh"])]
        data_dict["ftypo"]=[row[:] for i in range( data_dict["fgv"])]
    
    else:
        if key == "ftypo":
            ftypo=str(bin(int(data_dict["ftypo"], 32)))[2:]
            ftypo=[ftypo[i * data_dict["fgh"] : (i+1)*data_dict["fgh"]] for i in range(data_dict["fgv"])]
            ftypo=[[int(c) for c in chars] for chars in ftypo]

            data_dict["base_objects"]=2

        else:
            key_remainder=int(key.replace("ftypo", ''))

            data_dict["base_objects"]=int(2**key_remainder)

            ftypo=data_dict[key].split('_')
            ftypo=[baseconvert(int(chars, 36), 2**key_remainder) for chars in ftypo]
            ftypo=[[int(c) for c in str(number)] for number in ftypo]

    data_dict["ftypo"]=ftypo

    return data_dict

def string_reader(string):
    """function that reads the string and turns it into a readable dict"""

    loc_dict=string_to_dict(string)

    for boolean_tag in ["mirrh", "mirrv", "konh", "konv"]:
        try:
            loc_dict[boolean_tag]=bool(int(loc_dict[boolean_tag]))
        except:
            try:
                print("wrong boolean_tag {} : {}".format(boolean_tag, loc_dict[boolean_tag] ) )
            except:
                print("non present boolean_tag {}".format(boolean_tag) )

    for integer_tag in ["fgv", "fgh", "fp", "roth", "rotv"]:
        try:
            loc_dict[integer_tag]=int(loc_dict[integer_tag])
        except:
            try:
                print("wrong integer_tag {} : {}".format(integer_tag, loc_dict[integer_tag] ) )
            except:
                print("non present integer_tag {}".format(integer_tag) )

    for float_tag in ["frat", "c00", "c01", "c10", "c11"]:
        try:
            loc_dict[float_tag]=float(loc_dict[float_tag])
        except:
            try:
                print("wrong float_tag {} : {}".format(float_tag, loc_dict[float_tag] ) )
            except:
                print("non present float_tag {}".format(float_tag) )

    try:
        coords=loc_dict["mid"].split("%2C")
        coords=[c.replace('\n', '') for c in coords]
        for i, c in enumerate(coords):
            if (c is None) or (c==''):
                coords[i]=None
            else:
                coords[i]=float(c)
        loc_dict["mid"]=coords
        loc_dict["a"]=coords[0]
        # loc_dict["b"]=coords[1]
        loc_dict["b"]=1.-coords[1]  #transforming from negativly oriented to positive coordinate system
        loc_dict["hc_rel"]=coords[2]
    except: 
        print("no mid tag present")

    hs = []
    for h_tag in ["c01", "c11", "c10", "c00"]:
        try:
            hs.append(loc_dict[h_tag])

        except:
            print("no tag {} found in this data_dict".format(h_tag))

    loc_dict["hs"]=hs

    loc_dict=ftypo_handling(loc_dict)
    print("ftypo handled")

    return loc_dict

if __name__ == "__main__":
    string = "https://facademaker.alucobond.com/?ft=d2&fp=0&fgv=5&fgh=7&frat=1.3953488372093024&ftypo=tvvvvvv&mirrh=0&mirrv=0&roth=0&rotv=0&konh=0&konv=0&mat=&c00=1&c01=0&c10=0&c11=0.7"
    print(string_reader(string))