# different type functions
# positively oriented coordinate system, every object is generated from the bottom left corner
# ordering of points is always counter clockwise
# side position bottom, right, top, left

# q1 -> single value
def simple_square(l, w, h = .2):
    return [
        [0,0,h],
        [l,0,h],
        [l,w,h],
        [0,w,h]
    ]

def simple_square_with_b_pt(b_pt, l, w, h):
    return [
        [b_pt[0]    ,b_pt[1]    ,h],
        [b_pt[0] + l,b_pt[1]    ,h],
        [b_pt[0] + l,b_pt[1] + w,h],
        [b_pt[0]    ,b_pt[1] + w,h]
    ]

# q1Lift -> side lift
def one_side_lifted(l, w, side = 0, h0 = .2, h1 = 1.0):
    pts = [
        [0,0,h0],
        [l,0,h0],
        [l,w,h0],
        [0,w,h0]
    ]

    for i in range(2):
        pts[(i + side)%4][2] = h1

    return pts

# d2
def all_side_lifted(l, w, h0, h1, h2, h3):
    return [
        [0,0,h0],
        [l,0,h1],
        [l,w,h2],
        [0,w,h3]
    ]

# d4 -> centerpoint
def centerpoint(l, w, a, b, h0, h1):
    return simple_square(l,w,h0), [l * a, w * a, h1]

# q4
def four_squares(l, w, a, b, h0, h1, h2, h3):
    h_list = [[h0, h1], [h3, h2]]
    x_base = [0, a * l]
    l_list = [a * l, (1.0 - a) * l]
    y_base = [0, b * w]
    w_list = [b * w, (1.0 - b) * w]
    
    global_list = []
    for i, x in enumerate(x_base):
        row_list = []
        l = l_list[i]
        for j, y in enumerate(y_base):
            row_list.append(simple_square_with_b_pt([x, y], l, w_list[j], h_list[i][j]))

        global_list.append(row_list)

    return global_list