FUNCTION_TYPES={
    'd2': 'square',             # normal square
    'q1lift': 'square',         # square with a lifted side
    'd4': 'pyramid',            # pyramid
    'q4': 'quad_group',         # group of four quads
    't1': 'triangle',           # isosceles triangle
    't2': 'triangle',           # rightangle triangle
    't3': 'diamond',            # 2 triangles grouped side by side
    't4': 'square',             # with shift
}

FUNCTION_SHIFT_VALUES={
    'd2': 0.,
    'q1lift': 0.,
    'd4': 0.,
    'q4': 0.,
    't1': .5,
    't2': 0.,
    't3': 0.,
    't4': .5,
}

DEFAULT_DICT={
    'ft': 't2',                                     # function type, defining the complexity and which objects to use
    'fgh': 7,                                       # amount of panels in horizontal direction
    'fgv': 5,                                       # amount of panels in vertical direction
    'frat': 1.395,                                  # proportion of the leght and height of the panel elements
    'ftypo2': '1h9u1h_1h9u1h_1h9u1h_1h9u1h_1h9u1h', # for reference, not present if only an ftypo 2 is given
    'ftypo': [                                      # obj mask used for the facade
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    ],
    'mirrh': True,                                  # whether the point set is mirrored horizontally (heights + fold)
    'mirrv': True,                                  # whether the point set is mirrored vertically   (heights + fold)
    'konh': True,                                   # whether the direction of the fold is switched horizontally (pyramid: inside / outside, square: different diagonal)
    'konv': True,                                   # whether the direction of the fold is switched vertically   (pyramid: inside / outside, square: different diagonal)
    'roth': 0,                                      # whether the point set is rotated horizontally (heights + fold)
    'rotv': 0,                                      # whether the point set is rotated vertically   (heights + fold)
    'fp': 0,                                        # ???
    'c00': 0.0,                                     # bottom left corner height
    'c01': 0.0,                                     # top left corner height
    'c10': 0.69999999999999996,                     # bottom right corner height
    # 'c11': 0.0,                                     # top right corner height
    'hs': [0.0, 0.0, 0.69999999999999996],          # list of all heights, clockwise
    'mat': '',                                      # material tag - not used
}
