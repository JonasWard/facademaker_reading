from Rhino.Geometry import Point3d

def list_counter(input_list=[]):
    string=''

    if isinstance(input_list, list):
        string='\n'.join(['[']+[
            '\n'.join(['  '+s_str for s_str in list_counter(item).split('\n')])
            for item in input_list]+[']'])
    elif isinstance(input_list, Point3d):
        string=str("x:{}, y:{}, z:{}".format(
            input_list.X,
            input_list.Y,
            input_list.Z
        ))
    else:
        string=str(input_list)
        
    return string

if __name__ == "__main__":
    print(list_counter([[0,[0,[123,456], [23, 4]]]]))